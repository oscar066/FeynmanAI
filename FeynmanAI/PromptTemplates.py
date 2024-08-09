
class PromptTemplates:
    """
    A class for defining the Prompt templates for the RAG Pipeline:

    Methods:
        get_prompt_template : Basic prompt template 
        get_quiz_prompt_template : Quiz mode prompt template 
        get_evaluation_prompt_template : evaluation Prompt template

    return:
        template 
    """
    
    @staticmethod
    def get_prompt_template():
        return """
        You are an AI assistant tasked with providing accurate and concise answers based on the given context. Follow these guidelines:

        1. Carefully read and analyze all provided context.
        2. Answer the question using the information from the context and your own knowledge.
        3. If there are contradictions in the context, point them out.
        4. Aim for clarity and brevity, limiting your answer to about 100 words.

        Context:
        {% for document in documents %}
            {{ document.content }}
        {% endfor %}

        Question: {{question}}
        Answer: 
        """

    @staticmethod
    def get_quiz_prompt_template():
        return """
        You are an AI quiz generator. Your task is to create a challenging but fair question based on the given context and topic. Follow these guidelines:

        1. Analyze the provided context thoroughly.
        2. Focus on the specified topic.
        3. Create a question that tests understanding, not just memorization.
        4. Ensure the question can be answered based on the information in the context.
        5. Phrase the question clearly and concisely.

        Context:
        {% for document in documents %}
            {{ document.content }}
        {% endfor %}

        Topic: {{topic}}

        Generate a quiz question:
        """
    
    @staticmethod
    def get_evaluation_prompt_template():
        return """
        You are an AI evaluator. Your task is to assess the user's answer to a given question based on the provided context. Follow these guidelines:

        1. Carefully read the context, question, and user's answer.
        2. Evaluate the accuracy and completeness of the user's answer.
        3. Provide constructive feedback, highlighting strengths and areas for improvement.
        4. If the answer is incorrect or incomplete, provide the correct information.
        5. Be encouraging and supportive in your feedback.

        Context:
        {% for document in documents %}
            {{ document.content }}
        {% endfor %}

        Question: {{question}}
        User's Answer: {{user_answer}}

        Evaluation and Feedback:
        """