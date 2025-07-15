import requests
import json
import csv

# Headers copied from your browser to bypass NBA API blocks
headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'https://www.nba.com',
    'Referer': 'https://www.nba.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-gpc': '1',
}

# Parameters for the stat query
params = {
    'College': '',
    'Conference': '',
    'Country': '',
    'DateFrom': '',
    'DateTo': '',
    'Division': '',
    'DraftPick': '',
    'DraftYear': '',
    'GameScope': '',
    'Height': '',
    'ISTRound': '',
    'LastNGames': '0',
    'LeagueID': '00',
    'Location': '',
    'Month': '0',
    'OpponentTeamID': '0',
    'Outcome': '',
    'PORound': '0',
    'PerMode': 'PerGame',
    'PlayerExperience': '',
    'PlayerOrTeam': 'Player',
    'PlayerPosition': '',
    'PtMeasureType': 'Possessions',
    'Season': '2024-25',
    'SeasonSegment': '',
    'SeasonType': 'Playoffs',
    'StarterBench': '',
    'TeamID': '0',
    'VsConference': '',
    'VsDivision': '',
    'Weight': '',
}

# Send request
print("🔄 Sending request to NBA stats API...")
response = requests.get('https://stats.nba.com/stats/leaguedashptstats', params=params, headers=headers)
print("Status code:", response.status_code)

try:
    data = response.json()
    print("✅ JSON parsed successfully")

    # Check for expected keys
    if "resultSets" not in data or not data["resultSets"]:
        print("⚠️ No resultSets found.")
        print("Raw JSON:", json.dumps(data, indent=2))
        exit()

    # Extract header and data rows
    result_set = data["resultSets"][0]
    headers = result_set["headers"]
    rows = result_set["rowSet"]

    if not rows:
        print("⚠️ No data returned for the given parameters.")
        exit()

    print(f"✅ Retrieved {len(rows)} player rows\n")

    # Print first 5 players
    for row in rows[:5]:
        player = dict(zip(headers, row))
        print(player)

    # Save to CSV
    filename = "nba_touch_stats_2024_playoffs.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(zip(headers, row)))
    print(f"\n📁 Data saved to {filename}")

except Exception as e:
    print("❌ Error:", e)
    print("Response snippet:", response.text[:500])
