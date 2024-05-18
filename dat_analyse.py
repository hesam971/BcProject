import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as snsf
import numpy as np
from collections import defaultdict

# Load JSON data from the file
with open('nameOfJsonFile', 'r') as json_file:
    json_data = json.load(json_file)

# 1. Visualize 'trackingData' part in a bar chart
class SectionDataVisualizer:
    def __init__(self, section_data):
        self.section_names = set()
        self.section_times = defaultdict(list)
        self.data_for_boxplot = []
        # Sorting data base on names
        for message in section_data:
            for section in message['message']['trackingData']['sections']:
                section_name = section['section']
                time_spent = section['timeSpent']

                self.section_names.add(section_name)
                self.section_times[section_name].append(time_spent)

        self.data_for_boxplot = [self.section_times[section] for section in self.section_names]

    def visualize_data(self):
        plt.figure(figsize=(10, 6))
        plt.boxplot(self.data_for_boxplot, labels=list(self.section_names))
        plt.title('Boxplot of Time Spent in Different Sections')
        plt.xlabel('Sections')
        plt.ylabel('Time Spent (seconds)')
        plt.show()

    def calculate_spread(self):
        spread_data = {section: np.std(times) for section, times in self.section_times.items()}
        return spread_data

    def visualize_spread_pie_chart(self):
        spread_data = self.calculate_spread()

        labels = [f"{section} (Section {i+1})" for i, (section, spread) in enumerate(spread_data.items())]
        values = list(spread_data.values())

        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title('Spread (Standard Deviation) in Different Sections')
        plt.show()


# Usage:
json_file_path = 'nameOfJsonFile'

with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)

visualizer = SectionDataVisualizer(json_data)
visualizer.visualize_data()
visualizer.visualize_spread_pie_chart()


# 2. Visualize 'votingData' part in bar charts for likes and dislikes
# Extract voting data from each message
class VotingDataVisualizer:
    def __init__(self, json_data):
        self.voting_data = [message["message"]["votingData"] for message in json_data]
        self.section_totals = defaultdict(lambda: {"likes": 0, "dislikes": 0})
        self.prepare_data()

    def prepare_data(self):
        for section_data in self.voting_data:
            for section_id, votes in section_data.items():
                likes = votes["likes"]
                dislikes = votes["dislikes"]

                self.section_totals[section_id]["likes"] += likes
                self.section_totals[section_id]["dislikes"] += dislikes

    def calculate_spread(self):
        spread_data = {
            section_id: np.std([votes["likes"], votes["dislikes"]])
            for section_id, votes in self.section_totals.items()
        }
        return spread_data

    def visualize_spread_pie_chart(self):
        spread_data = self.calculate_spread()

        labels = list(spread_data.keys())
        values = list(spread_data.values())

        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title('Spread (Standard Deviation) in Votes for Each Section')
        plt.show()

    def visualize_votes_bar_chart(self):
        section_labels = [f"Section {section_id}" for section_id in self.section_totals.keys()]
        likes_values = [total["likes"] for total in self.section_totals.values()]
        dislikes_values = [total["dislikes"] for total in self.section_totals.values()]

        x = range(len(section_labels))

        plt.figure(figsize=(10, 6))
        plt.bar(x, likes_values, label='Likes', color='blue', width=0.4)
        plt.bar([i + 0.4 for i in x], dislikes_values, label='Dislikes', color='red', width=0.4)
        plt.xlabel('Section')
        plt.ylabel('Votes')
        plt.title('Likes and Dislikes by Section')
        plt.xticks([i + 0.2 for i in x], section_labels)
        plt.legend()
        plt.tight_layout()
        plt.show()

# Usage:
json_file_path = 'nameOfJsonFile'

with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)

voting_visualizer = VotingDataVisualizer(json_data)
voting_visualizer.visualize_votes_bar_chart()
voting_visualizer.visualize_spread_pie_chart()


# 3. Visualize 'firstInteractionTime' part in a bar chart
class FirstInteractionTimeVisualizer:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.first_interaction_times = {}

    def load_data(self):
        with open(self.json_file_path, 'r') as json_file:
            json_data = json.load(json_file)

        for item in json_data:
            first_interaction_time = item['message']['firstInteractionTime']

            for section, time in first_interaction_time.items():
                if section not in self.first_interaction_times:
                    self.first_interaction_times[section] = []

                self.first_interaction_times[section].append(float(time))

    def calculate_average_interaction_times(self):
        avg_interaction_times = {key: np.mean(values) for key, values in self.first_interaction_times.items()}
        return avg_interaction_times

    def calculate_spread(self):
        spread_data = {key: np.std(values) for key, values in self.first_interaction_times.items()}
        return spread_data

    def visualize_data_boxplot(self):
        values = list(self.first_interaction_times.values())

        plt.figure(figsize=(8, 6))
        plt.boxplot(values, labels=list(self.first_interaction_times.keys()))
        plt.xlabel('Sections')
        plt.ylabel('First Interaction Time')
        plt.title('First Interaction Time for Sections (Boxplot)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def visualize_spread_pie_chart(self):
        spread_data = self.calculate_spread()

        labels = list(spread_data.keys())
        values = list(spread_data.values())

        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title('Spread (Standard Deviation) in First Interaction Time for Sections')
        plt.show()

# Usage:
json_file_path = 'nameOfJsonFile'

visualizer = FirstInteractionTimeVisualizer(json_file_path)
visualizer.load_data()
visualizer.visualize_data_boxplot()
visualizer.visualize_spread_pie_chart()


# 4. Visualize 'scrollDepth' and 'videoPercentage' as averages
# Extract scroll depths and video percentages
class MetricsVisualizer:
    def __init__(self, json_data):
        self.scroll_depths = []
        self.video_percentages = []

        for message in json_data:
            tracking_data = message['message']['trackingData']

            scroll_depth = tracking_data.get('scrollDepth', 0)
            video_percentage = tracking_data.get('videoPercentage', 0)

            self.scroll_depths.append(scroll_depth)
            self.video_percentages.append(video_percentage)

    def calculate_averages(self):
        average_scroll_depth = np.mean(self.scroll_depths)
        average_video_percentage = np.mean(self.video_percentages)

        return average_scroll_depth, average_video_percentage

    def calculate_spreads(self):
        spread_scroll_depth = np.std(self.scroll_depths)
        spread_video_percentage = np.std(self.video_percentages)

        return spread_scroll_depth, spread_video_percentage

    def visualize_scroll_depth_boxplot(self):
        plt.figure(figsize=(6, 6))
        plt.boxplot(self.scroll_depths)
        plt.title('Boxplot of Scroll Depth')
        plt.ylabel('Scroll Depth')
        plt.show()

    def visualize_video_percentage_boxplot(self):
        plt.figure(figsize=(6, 6))
        plt.boxplot(self.video_percentages)
        plt.title('Boxplot of Video Percentage')
        plt.ylabel('Video Percentage')
        plt.show()

    def visualize_scroll_depth_spread(self):
        spread_scroll_depth, _ = self.calculate_spreads()

        plt.figure(figsize=(6, 6))
        plt.pie([spread_scroll_depth], labels=['Scroll Depth'], autopct='%1.1f%%', startangle=140)
        plt.title('Spread (Standard Deviation) in Scroll Depth')
        plt.show()

    def visualize_video_percentage_spread(self):
        _, spread_video_percentage = self.calculate_spreads()

        plt.figure(figsize=(6, 6))
        plt.pie([spread_video_percentage], labels=['Video Percentage'], autopct='%1.1f%%', startangle=140)
        plt.title('Spread (Standard Deviation) in Video Percentage')
        plt.show()

# Read JSON data from file
with open('nameOfJsonFile') as f:
    json_data = json.load(f)

# Instantiate MetricsVisualizer with JSON data
visualizer = MetricsVisualizer(json_data)

# Visualize scroll depth and video percentage separately
visualizer.visualize_scroll_depth_boxplot()
visualizer.visualize_video_percentage_boxplot()
visualizer.visualize_scroll_depth_spread()
visualizer.visualize_video_percentage_spread()


# 5. Visualize 'infoBoxInteractions' part
class SectionClickCounter:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.section_click_counts = {}

    def load_data(self):
        with open(self.json_file_path, 'r') as json_file:
            self.json_data = json.load(json_file)

    def count_section_clicks(self):
        for item in self.json_data:
            info_box_interactions = item['message']['infoBoxInteractions']

            for section in info_box_interactions:
                self.section_click_counts[section] = self.section_click_counts.get(section, 0) + 1

    def visualize_clicks(self):
        sections = list(self.section_click_counts.keys())
        click_counts = list(self.section_click_counts.values())

        plt.figure(figsize=(8, 6))
        plt.bar(sections, click_counts)
        plt.xlabel('Sections')
        plt.ylabel('Number of Clicks')
        plt.title('Clicks per Section (Info Box Interactions)')
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
        plt.tight_layout()
        plt.show()

# Usage:
json_file_path = 'nameOfJsonFile'  # Update with your JSON file path
click_counter = SectionClickCounter(json_file_path)
click_counter.load_data()
click_counter.count_section_clicks()
click_counter.visualize_clicks()


# 6. Visualize 'keywordClickInteractions' part
class KeywordClickCounter:
    def __init__(self, json_data):
        self.json_data = json_data
        self.keyword_click_counts = defaultdict(int)

    def count_keyword_clicks(self):
        # Loop through each message in the JSON data
        for item in self.json_data:
            keyword_click_interactions = item['message']['keywordClickInteractions']

            # Loop through each section in keywordClickInteractions
            for section, interactions in keyword_click_interactions.items():
                # Loop through each interaction in the section
                for interaction in interactions:
                    keyword = interaction['keyword']
                    # Increment the count for the keyword in the dictionary
                    self.keyword_click_counts[keyword] += 1

    def visualize_keyword_clicks(self):
        # Extract keywords and their respective counts
        keywords = list(self.keyword_click_counts.keys())
        counts = list(self.keyword_click_counts.values())

        # Create a bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(keywords, counts)
        plt.xlabel('Keywords')
        plt.ylabel('Number of Clicks')
        plt.title('Keyword Click Interactions')
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
        plt.tight_layout()
        plt.show()

# Usage:
json_file_path = 'nameOfJsonFile'

with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)

click_counter = KeywordClickCounter(json_data)
click_counter.count_keyword_clicks()
click_counter.visualize_keyword_clicks()