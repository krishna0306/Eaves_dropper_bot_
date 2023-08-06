import sqlite3
from datetime import datetime, timedelta

def parse_datetime(string_datetime):
    return datetime.strptime(string_datetime, '%Y-%m-%d %H:%M:%S')

def calculate_time_spent(start_time, end_time):
    time_spent = end_time - start_time
    return time_spent.total_seconds()

def main():
    # Replace 'path/to/your/Chrome/Profile' with the actual path to your Chrome profile folder.
    chrome_history_path = 'C:/Users/hp/AppData/Local/Google/Chrome/User Data/Default/History'

    # Connect to the Chrome history database
    conn = sqlite3.connect(chrome_history_path)
    cursor = conn.cursor()

    # Query to retrieve browsing history data
    query = "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC"
    cursor.execute(query)

    websites = {}
    current_date = None
    output_string = ""

    application_usage = {}

    for url, title, last_visit_time in cursor.fetchall():
        last_visit_time = datetime(1601, 1, 1) + timedelta(microseconds=last_visit_time)

        # Format time in 12-hour format with AM or PM
        formatted_time = last_visit_time.strftime('%I:%M:%S %p')

        if current_date is None or current_date != last_visit_time.date():
            current_date = last_visit_time.date()
            output_string += f"\nVisited sites on {current_date.strftime('%d %B %Y')}:\n\n"

        if url in websites:
            websites[url]['time_spent'] += calculate_time_spent(websites[url]['last_visit_time'], last_visit_time)
        else:
            websites[url] = {'title': title, 'last_visit_time': last_visit_time, 'time_spent': 0}

        websites[url]['last_visit_time'] = last_visit_time

        output_string += f"Website: {url}\nTitle: {title}\nTime of Visit: {formatted_time}\nTime Spent: {websites[url]['time_spent']:.2f} seconds\n\n"

        # Track application usage
        application_name = title.split('-')[0].strip()  # Extract application name from the title
        if application_name in application_usage:
            application_usage[application_name] += calculate_time_spent(websites[url]['last_visit_time'], last_visit_time)
        else:
            application_usage[application_name] = calculate_time_spent(websites[url]['last_visit_time'], last_visit_time)

    # Close the database connection
    conn.close()

    # Calculate overall usage
    overall_usage = sum(application_usage.values())

    # Add the overall usage and application-wise usage to the output string
    output_string += "\nOverall Usage:\n"
    output_string += f"Total Time Spent: {overall_usage:.2f} seconds\n\n"

    for application_name, usage_time in application_usage.items():
        output_string += f"{application_name} Usage: {usage_time:.2f} seconds\n"

    # Write the output to a text file
    output_file_path = 'C:/Users/hp/Desktop/browsing_history_output.txt'
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(output_string)

if __name__ == "__main__":
    main()
