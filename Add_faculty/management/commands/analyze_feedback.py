from django.core.management.base import BaseCommand
from Add_faculty.models import Evaluation, Faculty
from textblob import TextBlob
import re  # Importing the re module for regular expression operations

# Define your custom command class
class Command(BaseCommand):
    help = 'Analyze overall feedback for each faculty member using TextBlob'

    # Define the handle method to execute the command
    def handle(self, *args, **kwargs):
        # Define the set of offensive words and phrases
        offensive_phrases = ["putang ina", "putangina", "putang ina"]
        offensive_words = ["crap", "idiot", "stupid", "fool", "fuck", "fuck you","go to hell",
                           "fuck her", "fuck him", "shit", "bitch", "cunt",
                           "son of a bitch", "dickhead", "tanga", "mulala",
                           "gago", "inutil", "mang mang", "mangmang", "inotil",
                           "bobo"]

        faculties = Faculty.objects.all()

        for faculty in faculties:
            self.stdout.write(f'Analyzing overall feedback for Faculty ID: {faculty.id_number}, {faculty.first_name} {faculty.last_name}')

            # Retrieve evaluations associated with the faculty
            evaluations = Evaluation.objects.filter(faculty=faculty)

            # Initialize variables to store overall sentiment scores
            total_polarity = 0
            total_subjectivity = 0
            num_evaluations = 0
            offensive_feedback = []

            # Analyze feedback for each evaluation
            for evaluation in evaluations:
                # Preprocess feedback text to remove special characters and ensure case insensitivity
                cleaned_feedback = re.sub(r'[^\w\s]', '', evaluation.feedback.lower())

                # Perform sentiment analysis
                blob = TextBlob(cleaned_feedback)
                polarity = blob.sentiment.polarity
                subjectivity = blob.sentiment.subjectivity

                # Accumulate sentiment scores
                total_polarity += polarity
                total_subjectivity += subjectivity
                num_evaluations += 1

                # Check for offensive words and phrases
                for word in blob.words:
                    if word in offensive_words:
                        offensive_feedback.append(evaluation.feedback)
                        break  # No need to continue checking once an offensive word is found

                for phrase in offensive_phrases:
                    if phrase in cleaned_feedback:
                        offensive_feedback.append(evaluation.feedback)
                        break  # No need to continue checking once an offensive phrase is found

            # Calculate average sentiment scores
            if num_evaluations > 0:
                average_polarity = total_polarity / num_evaluations
                average_subjectivity = total_subjectivity / num_evaluations

                # Determine overall sentiment label
                if average_polarity > 0.1:
                    overall_sentiment_label = 'Positive'
                    sample_feedback = "The faculty member is doing an excellent job. Students appreciate their teaching style and find the lectures engaging."
                elif average_polarity < -0.1:
                    overall_sentiment_label = 'Negative'
                    sample_feedback = "The faculty member needs to improve their teaching approach. Students have expressed dissatisfaction with the course materials and delivery."
                else:
                    overall_sentiment_label = 'Neutral'
                    sample_feedback = "The feedback for this faculty member is mixed. Some students have positive comments, while others have suggestions for improvement."
                 

                # Print overall sentiment analysis results
                self.stdout.write(f'Overall Sentiment: {overall_sentiment_label} (Average Polarity: {average_polarity}, Average Subjectivity: {average_subjectivity})')

                # Print offensive feedback if any
                if offensive_feedback:
                    self.stdout.write('Offensive Feedback:')
                    for feedback in offensive_feedback:
                        self.stdout.write(f'- {feedback}')
                else:
                    self.stdout.write('No offensive feedback found.')

                self.stdout.write('\n')
            else:
                self.stdout.write('No evaluations found for this faculty member.')
