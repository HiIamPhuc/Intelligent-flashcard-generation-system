# NLPUngDung

# Website name: Memoria

## Framework:
- Front-end: React + TailwindCSS
    - UI kit: Hero UI (https://www.heroui.com/)
- Back-end: Django

## Requirements:
1. Create flashcards from different kinds of input:
    - Kinds of input:
        - Structured text
        - Unstructered text (docx, pptx, pdf)
    - From one document, create one topic (one user owns many flashcards)
    - Flashcard structure:
        - Vocabulary
        - Description
    - Creating configuration:
        - Number of flashcards created
    - Filter documents with risk of attack

2. Learn from flashcards:
    - User chooses a topic
        -> Each flashcard pops up to the screen. There will be 3 situations that can happen:
            - User have learnt the word -> Swipe to the right
            - User haven't learnt the word -> Swipe to the left
            - User wants to see the word's description -> Click on the card

3. History:
    - For each topic, save 3 informations:
        - Unlearnt words
        - Learnt words

4. Edit flashcards:
    - User can edit each flashcard in a topic and save.

5. Word pronunciation:
    - For each flashcard, user can click on the Speaker button to display IPA of the word.
    - If user wants to listen to pronunciation of the word, click on the "Play" button next to the IPA.
        -> Pronunciation learning

6. Pronunciation learning:
    - If user wants to check his/her pronunciation and compare it with the word pronunciation, click on "Check your pronunciation".
    - System checks user's pronunciation and score it, then send it back to user. User can retry pronunciation checking to reach a higher score.

7. QnA Chatbot:
    - If user wants to ask about a vocabulary in any topic they have created, user can use Chatbot to ask.
    - Chatbot will answer to user information about the word user asked. Note that all information the chatbot answers is from the document user submit, not related to any extra information.