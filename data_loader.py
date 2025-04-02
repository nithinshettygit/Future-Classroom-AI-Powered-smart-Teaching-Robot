import json
from pathlib import Path
from typing import List, Dict, Tuple

class DataLoader:
    @staticmethod
    def load_data(filepath: Path) -> List[Dict]:
        """Load and validate JSON files"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else [data]

    @staticmethod
    def prepare_topic_data(data: List[Dict]) -> Tuple[List[str], List[Dict]]:
        """Process topics from integrated.json"""
        texts = []
        id_map = []
        for day in data:
            day_label = f"Day {day.get('day_number', '')}"
            for topic in day.get('topics', []):
                if topic.get('content'):
                    text = f"{topic['chapter']} {topic['subchapter']}: {topic['content']}"
                    texts.append(text)
                    id_map.append({
                        **topic,
                        'day': day_label,
                        'date': day.get('date')
                    })
        return texts, id_map

    @staticmethod
    def prepare_figure_data(data: List[Dict]) -> Tuple[List[str], List[Dict]]:
        """Process figures from integrated.json"""
        texts = []
        id_map = []
        for day in data:
            day_label = f"Day {day.get('day_number', '')}"
            for topic in day.get('topics', []):
                for fig in topic.get('figures', []):
                    full_text = f"{fig['figure']}: {fig['description']}"
                    texts.append(full_text)
                    id_map.append({
                        'figure': fig['figure'],
                        'description': fig['description'],
                        'chapter': topic['chapter'],
                        'subchapter': topic['subchapter'],
                        'day': day_label,
                        'date': day.get('date')
                    })
        return texts, id_map