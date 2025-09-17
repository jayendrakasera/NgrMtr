"""
Simple rule-based AI classification system for categorizing civic issues
In production, this could be replaced with machine learning models
"""
import re
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from models.department import Department

class IssueClassifier:
    def __init__(self, db: Session):
        self.db = db
        self._load_department_keywords()
    
    def _load_department_keywords(self):
        """Load department keywords from database"""
        self.department_keywords = {}
        departments = self.db.query(Department).filter(Department.is_active == True).all()
        
        for dept in departments:
            if dept.keywords:
                keywords = [kw.strip().lower() for kw in dept.keywords.split(',')]
                self.department_keywords[dept.id] = {
                    'name': dept.name,
                    'keywords': keywords
                }
    
    def classify_issue(self, title: str, description: str) -> Tuple[Optional[int], float, bool]:
        """
        Classify an issue and return (department_id, confidence, needs_manual_review)
        
        Args:
            title: Issue title
            description: Issue description
            
        Returns:
            Tuple of (department_id, confidence_score, needs_manual_review)
        """
        text = f"{title} {description}".lower()
        
        # Remove punctuation and split into words
        words = re.findall(r'\b\w+\b', text)
        word_set = set(words)
        
        # Calculate match scores for each department
        dept_scores = {}
        
        for dept_id, dept_info in self.department_keywords.items():
            keywords = dept_info['keywords']
            matches = sum(1 for keyword in keywords if keyword in word_set)
            
            if matches > 0:
                # Calculate confidence based on keyword matches
                confidence = min(matches / len(keywords), 1.0)
                dept_scores[dept_id] = confidence
        
        if not dept_scores:
            # No matches found - needs manual review
            return None, 0.0, True
        
        # Get department with highest score
        best_dept_id = max(dept_scores, key=dept_scores.get)
        best_confidence = dept_scores[best_dept_id]
        
        # If confidence is too low, flag for manual review
        needs_manual_review = best_confidence < 0.3
        
        # Boost confidence for multiple keyword matches
        if best_confidence >= 0.5:
            best_confidence = min(best_confidence + 0.2, 1.0)
        
        return best_dept_id, best_confidence, needs_manual_review
    
    def get_category_suggestions(self, text: str, limit: int = 3) -> list:
        """Get category suggestions for given text"""
        words = re.findall(r'\b\w+\b', text.lower())
        word_set = set(words)
        
        suggestions = []
        
        for dept_id, dept_info in self.department_keywords.items():
            keywords = dept_info['keywords']
            matches = sum(1 for keyword in keywords if keyword in word_set)
            
            if matches > 0:
                confidence = matches / len(keywords)
                suggestions.append({
                    'department_id': dept_id,
                    'department_name': dept_info['name'],
                    'confidence': confidence,
                    'matched_keywords': [kw for kw in keywords if kw in word_set]
                })
        
        # Sort by confidence and return top suggestions
        suggestions.sort(key=lambda x: x['confidence'], reverse=True)
        return suggestions[:limit]

def get_classifier(db: Session) -> IssueClassifier:
    """Get classifier instance"""
    return IssueClassifier(db)