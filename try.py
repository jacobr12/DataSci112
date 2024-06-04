import requests
from bs4 import BeautifulSoup
import datetime
import csv

def fetch_transcript(date):
    url = f"https://transcripts.cnn.com/show/sn/date/{date}/segment/01"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        transcript_parts = soup.find_all('p', {'class': 'cnnBodyText'})
        if len(transcript_parts) >= 3:
            transcript = transcript_parts[2].get_text()
            return transcript
        else:
            print(f"No transcript found for {date}")
            return None
    else:
        print(f"Failed to fetch {date}")
        return None

def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + datetime.timedelta(n)

def main():
    start_date = datetime.date(2011, 8, 22) 
    end_date = datetime.date(2024, 5, 24)    

    with open('cnn10_transcripts.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Date', 'Transcript'])
        for single_date in date_range(start_date, end_date):
            date_str = single_date.strftime("%Y-%m-%d")
            transcript = fetch_transcript(date_str)
            if transcript:
                csvwriter.writerow([date_str, transcript])

if __name__ == "__main__":
    main()
