import gpt
import time
import re  # Import the regular expression module

def process(topic_list, include_code=True):
    data_list = []
    for topic in topic_list:
        dct = {}
        prompt = f"""
        Generate comprehensive, in-depth information about: **{topic}**.  Output *strictly* the following JSON-like format.  Do *not* include *any* additional text outside the delimiters.

        <<<TOPIC>>>
        [Topic Title:  A concise, descriptive title for the topic]
        <<<TOPIC>>>
        <<<SUMMARY_START>>>
        [Summary Sentence 1:  A complete, informative sentence.]
        [Summary Sentence 2:  Another complete, informative sentence, building on the previous one.]
        [Summary Sentence 3:  (and so on, for at least 10 sentences)]
        ...
        [Summary Sentence 10:  A concluding sentence summarizing the core idea.]
        <<<SUMMARY_END>>>

        **Requirements:**

        *   **Depth:**  The summary sentences MUST be in-depth, providing significant, non-trivial information.  Assume an audience that wants to learn *beyond* the basics. Each sentence should stand alone as a valuable piece of information.
        *   **Word Count:**  The combined summary sentences should be approximately 500-700 words.  This is a target, not a strict limit, but strive for substantial content.
        *   **Clarity:**  Each sentence must be grammatically correct, clear, and concise. Avoid jargon or overly complex phrasing unless it's essential to the topic (and then explain it briefly).
        *   **No Lists Within Sentences:** Absolutely NO numbered lists or bullet points *within* the individual summary sentences.  Each sentence must be a complete, flowing thought.
        *   **No Redundancy:** Avoid repeating information.  Each sentence should add a *new* aspect or detail.
        *   **Strict Format:** Adhere *exactly* to the delimiters. Any deviation will cause parsing errors.
        * **Factual Accuracy:** Ensure all information is factually accurate and up-to-date.
        * **Key Concepts:** Cover all *major* key concepts, principles, and applications related to the topic. Don't just skim the surface.

        """
        text = gpt.get_summarise(prompt, topic)
        #print(f"RAW TEXT:\n{text}") # Debugging

        try:
            # Use regular expressions for more robust parsing:
            match = re.search(r"<<<TOPIC>>>(.*?)<<<TOPIC>>>.*?<<<SUMMARY_START>>>(.*?)<<<SUMMARY_END>>>", text, re.DOTALL)
            if match:
                dct["Topic"] = match.group(1).strip()
                summary_text = match.group(2).strip()
                dct["Summary"] = [line.strip() for line in summary_text.split("\n") if line.strip() and line.startswith("[Summary Sentence")]
            else:
                raise ValueError("Could not find expected delimiters in response.")

            #print(dct)

        except Exception as e:
            print(f"Error parsing topic/summary for '{topic}': {e}")
            dct["Topic"] = f"Error parsing topic: {topic}"
            dct["Summary"] = [f"Error parsing summary: {e}"]


        dct["Code"] = ""  # Initialize
        if include_code:
            code_prompt = f"""
            Provide a *short*, relevant Python code snippet directly illustrating a *key* concept from the topic: '{topic}'.

            **Requirements:**

            *   **Relevance:** The code MUST be directly and clearly related to a significant aspect of the topic.  No generic examples.
            *   **Conciseness:**  Keep the code as short as possible while still being complete and functional.  Aim for 10-25 lines maximum.
            *   **Correctness:** The code MUST be syntactically correct and runnable Python code.
            *   **Output:** Return *ONLY* the code, surrounded by triple backticks, and *nothing* else:

            ```python
            # Your code here
            ```
            * **No Explanations:** Do not include any comments, explanations, or docstrings *within* the code.  The code should speak for itself.
            * **Best Practices:** Use good Pythonic style (e.g., meaningful variable names, proper indentation).
            """
            code = gpt.get_summarise(code_prompt, topic)
            #print(f"RAW CODE:\n{code}")

            try:
                # More robust code extraction:
                code_match = re.search(r"```python(.*?)```", code, re.DOTALL)
                if code_match:
                    dct["Code"] = code_match.group(1).strip()
                else:
                    dct["Code"] = "# Error: Could not extract code. Check prompt and response."
            except Exception as e:
                print(f"Error extracting code for '{topic}': {e}")
                dct["Code"] = f"# Error extracting code: {e}"

        data_list.append(dct)
        if len(topic_list) > 1:
            time.sleep(55)  # Consider using a more robust rate-limiting approach

    return data_list


def structured(topic_list, include_code=True):
    data_list = process(topic_list, include_code)
    structured_data = []
    for data in data_list:
        topic = data["Topic"]
        code = data.get("Code", "")
        summary = data.get("Summary", "")

        prompt = f"""
        Create a detailed presentation outline for the topic: '{topic}'. Structure the outline as a series of slides.

        **Overall Presentation Structure:**

        *   **Title:** Begin with a single line: `Title: [Concise Presentation Title]`
        *   **Slides:** Each slide should follow this format, separated by `---`:

            ```
            Slide [Number]: [Short, Descriptive Slide Title]
            - [Concise bullet point 1, summarizing a key idea]
            - [Concise bullet point 2, expanding on the previous point or introducing a new one]
            - [Concise bullet point 3, ... and so on, for 3-5 bullet points per slide]

            Image Suggestion: [A detailed description of an image that would visually represent the slide's content. Be *very* specific. Consider diagrams, charts, screenshots, or conceptual illustrations. Example: "A flowchart illustrating the X process", "A graph showing the relationship between Y and Z", "A screenshot of the A tool in action", "A conceptual diagram of B architecture".]
            ---
            ```

        *   **Code Slide:** If a code snippet is provided, include it in a separate slide immediately after the relevant content slide. Use the following format for the code slide:

            ```
            Slide [Number]: Code Example
            ```python
            [Code snippet here]
            ```
            ---
            ```

        **Requirements:**

        *   **Number of Slides:** Generate approximately 5-7 slides.
        *   **Slide Titles:** Keep slide titles very short and to the point.
        *   **Bullet Points:** Bullet points should be concise summaries, *not* full sentences. Use keywords and phrases. Aim for 10-20 words per bullet point.
        *   **Code Integration:** If a code snippet is provided, place it in a separate slide immediately after the relevant content slide.
        *   **Summary-Driven:** The content of the slides MUST be derived from the provided summary. Do not introduce new information not present in the summary.
        *   **Image Suggestions:** Provide a *detailed* and *specific* image suggestion after *every* slide. The image should *directly* relate to the slide's content.
        *   **No Conversational Text:** Ensure the output is professional and structured.

        **Provided Summary:**

        {summary}
        """
        if include_code and code:
            prompt += f"""
        **Code Snippet (Place in a separate slide):**

        ```python
        {code}
        ```
        """

        slide_data = gpt.get_summarise(prompt, topic)
        data["Slides"] = slide_data
        structured_data.append(data)
        time.sleep(20)  # Again, consider a more robust rate-limiting solution
    return structured_data