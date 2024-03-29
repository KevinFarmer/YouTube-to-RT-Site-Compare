from rapidfuzz import fuzz, utils
import csv

roosterteeth = dict()
youtube = dict()

with open('ALL_RT_Site_Videos.csv', encoding="utf-8-sig") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        roosterteeth[row[0]] = [row[1], row[2]]

with open('ALL_RT_YouTube_Videos.csv', encoding="utf-8-sig") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        youtube[row[0]] = [row[1], row[2]]

with open('output.csv', 'w', encoding="utf-8-sig", newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["YouTube IA Link","RoosterTeeth Site IA Link", "YouTube ID", "RoosterTeeth ID", "YouTube Title", "RoosterTeeth Title", "likeness"])

    counter = 0
    for itemYT in youtube:
        counter += 1
        if counter == 10000:
            print("a quarter of the way through")
        if counter == 20000:
            print("half way through")
        if counter == 30000:
            print("three quarters of the way through")
        if counter == 40000:
            print("almost done!")
        #print(youtube[itemYT][1])
        for itemRT in roosterteeth:
            likeness = fuzz.token_sort_ratio(itemYT,itemRT,processor=utils.default_process)
            if likeness > 85:
                #print(f"YouTube Title:{itemYT}, Rooster Teeth Title: {itemRT}, Comparison Value = {likeness}")
                writer.writerow([youtube[itemYT][1], roosterteeth[itemRT][1], youtube[itemYT][0], roosterteeth[itemRT][0], itemYT, itemRT, likeness])

#fuzz.token_set_ratio(itemYT,itemRT,processor=utils.default_process) # doesn't really work at all
#fuzz.token_sort_ratio(itemYT,itemRT,processor=utils.default_process) #works sort of well, needs likeness of 85+, struggles with numbers
#fuzz.QRatio(itemYT,itemRT,processor=utils.default_process) # works, kind of, 80+ likeness needed for semblance of working, struggles with numbers
