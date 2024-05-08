import json
import csv


def process_shows():
    shows = dict()
    with open(f'shows.json', 'r') as infile:
        shows = json.load(infile)

    print(f"Found {shows['count']} shows")

    with open('rt_shows.csv', 'w', encoding="utf-8-sig", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["id","title", "slug", "is_sponsors_only", "published_at", "channel_slug", "episode_count"])

        for show in shows['data']:
            print(show['id'])
            attr = show['attributes']
            writer.writerow([show['id'], attr["title"], attr["slug"], attr["is_sponsors_only"], attr['published_at'], attr["channel_slug"], attr["episode_count"]])

def process_watch():
    watch = dict()
    with open(f'watch.json', 'r') as infile:
        watch = json.load(infile)

    print(f"Found {watch['count']} episodes")
    data = watch["data"]

    with open('rt_watch.csv', 'w', encoding="utf-8-sig", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["type", "channel_slug", "show_title", "show_slug", "show_url", "season_number", "ep_number", "id", "title", "slug", "is_sponsors_only", "public_golive"])

        for video in data:
            id = str(video["id"])
            vid_type = video["type"]
            attr = video["attributes"]
            title = attr['title']
            slug = attr['slug']
            public_golive = attr['public_golive_at']
            channel_slug = attr['channel_slug']
            ep = attr['number']

            if vid_type == 'bonus_feature':
                id += "-bonus"
                show_title = attr['parent_content_title']
                show_slug = attr['parent_content_slug']
                season = ''
            else:
                show_title = attr['show_title']
                show_slug = attr['show_slug']
                season = attr['season_number']
                
            show_url = f"https://roosterteeth.com/series/{show_slug}"
            writer.writerow([vid_type, channel_slug, show_title, show_slug, show_url, season, ep, id, title, slug, attr["is_sponsors_only"], public_golive])
    print("Finishing writing to rt_watch.csv")

process_watch()
