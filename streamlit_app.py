import streamlit as st
import requests

st.title("GuildWars 2 - Achievment Hunters")

url = "https://api.guildwars2.com/v2/account/achievements"
ach_url = "https://api.guildwars2.com/v2/achievements"


def chunk(items, n):
    for i in range(0, len(items), n):
        yield items[i:i + n]

api_keys = st.text_input("API Keys")
key_list = api_keys.split(" ")

try:
    player_achievs = set()
    for key in key_list:
        headers = {"Authorization": f"Bearer {key}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        achievements = response.json()
        progressing = [str(ach["id"]) for ach in achievements if not ach["done"]]

        all_achvs = [name["name"] for c in chunk(progressing, 200) for name in requests.get(f"{ach_url}?ids={','.join(c)}").json()]
        player_achievs.update(set(all_achvs))


    data = "\n".join(sorted(player_achievs))
    st.markdown(
        "### All Commonly Uncompleted Achievements:\n" +
        "\n".join(f"- {a}" for a in sorted(player_achievs))
    )
except Exception as e:
    print("exc", e)