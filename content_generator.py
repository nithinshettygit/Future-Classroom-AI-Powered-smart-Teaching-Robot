import ollama
from pathlib import Path

class ContentGenerator:
    def __init__(self):
        self.model_name = "llama3.2"
        self.image_dir = Path("static/images")

    def _find_image_file(self, figure_name):
        """Find image with exact naming convention (Figure_1.1.png)"""
        base_name = figure_name.replace(' ', '_')
        for ext in ['.png', '.jpg', '.jpeg', '.svg']:
            path = self.image_dir / f"{base_name}{ext}"
            if path.exists():
                return f"/static/images/{base_name}{ext}"
        return None

    def generate_topic_explanation(self, content: str, subchapter: str) -> str:
        prompt = f"""Generate a well-formatted chemistry lesson explanation using Markdown:

        **Topic:** {subchapter}

        **Content:** {content}

        Format with these rules:
        1. Use ## for main headings
        2. Use ### for subheadings
        3. **Bold** important terms
        4. *Italicize* safety notes
        5. Use - for bullet points
        6. Separate concepts with blank lines
        7. Write chemical equations like: 2H₂ + O₂ → 2H₂O

        Include these sections:
        ## Key Concepts
        ## Chemical Process
        ## Observations
        ## Safety Considerations
        ## Real-world Applications"""

        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={'num_predict': 1024}
            )
            return response['response']
        except Exception as e:
            print(f"Explanation error: {e}")
            return content

    def generate_figure_explanation(self, figure_data: dict) -> dict:
        prompt = f"""Generate a detailed diagram explanation using Markdown:

        **Figure:** {figure_data['figure']}
        **Description:** {figure_data['description']}

        Format with:
        ### Components
        - List all parts with **bold** names
        ### Process
        1. Numbered steps
        2. Chemical changes
        ### Safety
        *Important precautions*
        ### Key Points
        - Scientific principles
        - Observations

        Include chemical equations where applicable."""

        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={'num_predict': 512}
            )
            explanation = response['response']
        except Exception as e:
            print(f"Figure explanation error: {e}")
            explanation = figure_data['description']

        return {
            'path': self._find_image_file(figure_data['figure']),
            'figure': figure_data['figure'],
            'description': figure_data['description'],
            'explanation': explanation,
            'subchapter': figure_data['subchapter']
        }