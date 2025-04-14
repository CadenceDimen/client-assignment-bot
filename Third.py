import pandas as pd

# 1. Load and clean the team data
latest_team_data = pd.read_excel("Team Profiles.xlsx", sheet_name="Team Data")
latest_team_data.columns = latest_team_data.columns.str.strip()
latest_team_data['Aptitude'] = latest_team_data['Aptitude'].str.extract(r'(\d)').astype(int)
latest_team_data['Communication'] = latest_team_data['Communication'].str.extract(r'(\d)').astype(int)
for lang in ['English', 'Spanish', 'Portuguese']:
    latest_team_data[lang] = latest_team_data[lang].str.strip().str.title()

# 2. Client Type to Service Mapping
client_type_to_service = {
    "1 - U.S. Corporation with Tax Services (2XXXXX) - Form 1120": "Form 1120",
    "2 - U.S. S-Corporation with Tax Services (2XXXXX) - Form 1120-S": "Form 1120-S",
    "3 - Foreign Corporation with Tax Services (2XXXXX) - Form 1120-F": "Form 1120-F",
    "4 - U.S. Partnership with Tax Services (2XXXXX) - Form 1065": "Form 1065 - U.S. Partnership",
    "5 - Foreign Partnership with Tax Services (2XXXXX) - Form 1065": "Form 1065 - Foreign Partnership",
    "6 - Non-Profit with Tax Services (2XXXXX)": "Non-Profit with Tax Services",
    "7 - Disregarded Entity DRE5472 (3XXXXX) - Form 5472/ Pro Form 1120": "Form 5472/Pro Form 1120 -DRE",
    "8 - US Individual Tax Services (4XXXX) - Form 1040": "Form 1040",
    "9 - NRA Individual Tax Services (4XXXX) - Form 1040NR": "Form 1040 NR",
    "10 - Fiduciary or Trust (6XXXXX)": "Fiduciary or Trust",
    "11 - Accounting Only- Any Company Type (7XXXXX)": "Accounting"
}

# 3. Filter by Tier Distribution
def filter_by_tier_distribution(team_df, client_profile):
    acct_limits = {
        'Real_Estate': 0.40,
        'Individuals': 0.20,
        'Operational': 0.20,
        'Accounting': 0.20
    }
    non_acct_limits = {
        'Real_Estate': 0.50,
        'Individuals': 0.25,
        'Operational': 0.25
    }
    tier = client_profile['Client_Tier']
    base_tier = 'Accounting' if 'Accounting' in tier else tier
    base_tier_col = base_tier.replace(" ", "_") + "_Count"

    def is_within_distribution(row):
        total_clients = row.get('Clients_Count', 1)
        current_count = row.get(base_tier_col, 0)
        current_pct = current_count / total_clients if total_clients > 0 else 0
        team_type = row['Is Accounting Team']
        limits = acct_limits if team_type else non_acct_limits
        max_pct = limits.get(base_tier, 1.0)
        return current_pct < max_pct

    return team_df[team_df.apply(is_within_distribution, axis=1)]

# 4. Main Matching Function
def match_client_to_team(team_df, client_profile):
    service = client_type_to_service.get(client_profile['Client_Type'], "Accounting")
    client_profile['Service'] = service

    team_df = team_df[~((team_df['BU'] == 'BU-Team PMedina') & (service != 'Accounting'))]

    if client_profile['Complexity'] == 'High':
        team_df = team_df[team_df['Aptitude'] == 5]
    elif client_profile['Complexity'] == 'Medium':
        team_df = team_df[team_df['Aptitude'] >= 4]
    else:
        team_df = team_df[team_df['Aptitude'] >= 1]
        team_df = team_df.sort_values(by='Billing')

    if client_profile['VIP'] == 'VIP':
        if client_profile['Complexity'] == 'High':
            team_df = team_df.sort_values(by='Aptitude', ascending=False)
            if (team_df['Communication'] == 5).any():
                team_df = team_df[team_df['Communication'] == 5]
        else:
            team_df = team_df.sort_values(by='Communication', ascending=False)

    if client_profile['Preferred_Location'] == 'Coral Gables':
        client_profile['Preferred_Location'] = 'Gables'
    if client_profile['Preferred_Location']:
        team_df = team_df[team_df['Office'] == client_profile['Preferred_Location']]

    lang = client_profile['Language']
    if lang in ['Spanish', 'English', 'Portuguese']:
        team_df = team_df[team_df[lang] == 'Yes']

    team_df = team_df[
        (team_df['Billing'] < 750000) &
        (team_df['Clients_Count'] < 250) &
        (team_df['Client Loss'] <= 0.20)
    ]

    if service == 'Accounting':
        team_df = team_df[team_df['Is Accounting Team'] == True]
        if client_profile['Client_Tier'] == 'Monthly Accounting':
            team_df = team_df[team_df['Monthly_Accounting'] < 10]
        elif client_profile['Client_Tier'] == 'Quarterly Accounting':
            team_df = team_df[team_df['Quarterly_Accounting'] < 10]

    team_df = filter_by_tier_distribution(team_df, client_profile)

    if not team_df.empty:
        team_df = team_df.sort_values(by='Client Loss')

    top5 = team_df.head(5)

    pref1 = top5[top5['Service Preference1'] == service]
    if not pref1.empty:
        return pref1['Name'].tolist()

    pref2 = top5[top5['Service Preference2'] == service]
    if not pref2.empty:
        return pref2['Name'].tolist()

    pref3 = top5[top5['Service Preference3'] == service]
    if not pref3.empty:
        return pref3['Name'].tolist()

    return top5['Name'].tolist() if not top5.empty else ["No team could be assigned."]

# 5. Return Detailed Info
def get_team_details(team_df, matched_names):
    result_df = team_df[team_df['Name'].isin(matched_names)][
        ['Name', 'Role', 'BU', 'Office', 'Partner_Manager']
    ].reset_index(drop=True)

    result_df.index += 1  # Start index from 1
    return result_df

