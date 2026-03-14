"""
TRUMAN AI Events System
200+ life events across 9 pools for dynamic storytelling

[SF] Clean event management and selection
[AC] Atomic functions for event generation and impact
"""

import random
from typing import Dict, List, Optional, Tuple
from enum import Enum
from .config import PERSONALITY_TRAITS, CORE_DRIVES

class EventPool(Enum):
    """Categories of life events"""
    CAREER = "career"
    RELATIONSHIP = "relationship" 
    HEALTH = "health"
    FINANCE = "finance"
    EDUCATION = "education"
    SOCIAL = "social"
    FAMILY = "family"
    PERSONAL_GROWTH = "personal_growth"
    UNEXPECTED = "unexpected"

class LifeEvent:
    """Represents a single life event with impacts"""
    
    def __init__(self, title: str, description: str, pool: EventPool, 
                 mood_impact: float, trait_impacts: Dict[str, float],
                 drive_impacts: Dict[str, float], requirements: Optional[List[str]] = None):
        self.title = title
        self.description = description
        self.pool = pool
        self.mood_impact = mood_impact  # -1.0 to 1.0
        self.trait_impacts = trait_impacts  # trait_name: impact
        self.drive_impacts = drive_impacts  # drive_name: impact
        self.requirements = requirements or []
        
    def can_trigger(self, character_state: Dict) -> bool:
        """Check if event can trigger based on character state"""
        for req in self.requirements:
            if req not in character_state or not character_state[req]:
                return False
        return True

class EventEngine:
    """Manages life events and their triggering"""
    
    def __init__(self):
        self.events = self._initialize_events()
        self.recent_events = []  # Track recent events to avoid repetition
        
    def _initialize_events(self) -> Dict[EventPool, List[LifeEvent]]:
        """Initialize all 200+ life events across 9 pools"""
        events = {pool: [] for pool in EventPool}
        
        # CAREER EVENTS (25 events)
        events[EventPool.CAREER] = [
            LifeEvent(
                "Promotion at Work",
                "Your hard work pays off with a well-deserved promotion.",
                EventPool.CAREER, 0.3,
                {"conscientiousness": 0.1, "achievement_striving": 0.2},
                {"achievement": 0.3, "power": 0.1},
                ["has_job"]
            ),
            LifeEvent(
                "New Job Opportunity",
                "An exciting new career opportunity presents itself.",
                EventPool.CAREER, 0.2,
                {"openness": 0.1, "extraversion": 0.1},
                {"achievement": 0.2, "stimulus": 0.1},
                ["has_job"]
            ),
            LifeEvent(
                "Workplace Conflict",
                "A disagreement with a colleague creates tension at work.",
                EventPool.CAREER, -0.2,
                {"agreeableness": -0.1, "neuroticism": 0.1},
                {"power": -0.1, "affiliation": -0.1},
                ["has_job"]
            ),
            LifeEvent(
                "Successful Project",
                "Your project exceeds expectations and impresses management.",
                EventPool.CAREER, 0.4,
                {"conscientiousness": 0.2, "competence": 0.1},
                {"achievement": 0.4, "power": 0.1},
                ["has_job"]
            ),
            LifeEvent(
                "Job Loss",
                "The company downsizes and you lose your position.",
                EventPool.CAREER, -0.5,
                {"neuroticism": 0.3, "self_discipline": -0.1},
                {"achievement": -0.3, "security": -0.4},
                ["has_job"]
            ),
            LifeEvent(
                "Mentorship Opportunity",
                "A senior colleague offers to mentor you professionally.",
                EventPool.CAREER, 0.3,
                {"openness": 0.1, "achievement_striving": 0.1},
                {"achievement": 0.2, "affiliation": 0.1},
                ["has_job"]
            ),
            LifeEvent(
                "Business Trip",
                "You travel for work and gain new perspectives.",
                EventPool.CAREER, 0.1,
                {"openness": 0.2, "extraversion": 0.1},
                {"stimulus": 0.2, "achievement": 0.1},
                ["has_job"]
            ),
            LifeEvent(
                "Office Romance",
                "You develop feelings for a coworker.",
                EventPool.CAREER, 0.2,
                {"extraversion": 0.1, "neuroticism": 0.1},
                {"affiliation": 0.3, "romance": 0.2},
                ["has_job"]
            ),
            LifeEvent(
                "Workplace Recognition",
                "Your contributions are publicly acknowledged.",
                EventPool.CAREER, 0.3,
                {"self_esteem": 0.2, "extraversion": 0.1},
                {"achievement": 0.3, "power": 0.1},
                ["has_job"]
            ),
            LifeEvent(
                "Difficult Deadline",
                "A challenging deadline creates significant stress.",
                EventPool.CAREER, -0.2,
                {"neuroticism": 0.2, "anxiety": 0.1},
                {"achievement": -0.1, "security": -0.1},
                ["has_job"]
            ),
            LifeEvent(
                "Career Change",
                "You decide to pursue a completely different career path.",
                EventPool.CAREER, 0.0,
                {"openness": 0.3, "self_discipline": 0.1},
                {"stimulus": 0.3, "achievement": 0.0},
                ["has_job"]
            ),
            LifeEvent(
                "Startup Idea",
                "An innovative business idea captures your imagination.",
                EventPool.CAREER, 0.2,
                {"openness": 0.2, "achievement_striving": 0.2},
                {"achievement": 0.3, "power": 0.1},
                []
            ),
            LifeEvent(
                "Work-Life Balance Issues",
                "Long hours start affecting your personal life.",
                EventPool.CAREER, -0.3,
                {"neuroticism": 0.2, "self_discipline": -0.1},
                {"security": -0.2, "affiliation": -0.1},
                ["has_job"]
            ),
            LifeEvent(
                "Professional Certification",
                "You earn a valuable professional certification.",
                EventPool.CAREER, 0.3,
                {"conscientiousness": 0.2, "competence": 0.2},
                {"achievement": 0.3, "security": 0.1},
                ["has_job"]
            ),
            LifeEvent(
                "Networking Success",
                "A professional connection leads to new opportunities.",
                EventPool.CAREER, 0.2,
                {"extraversion": 0.2, "social": 0.1},
                {"achievement": 0.2, "affiliation": 0.2},
                ["has_job"]
            ),
            LifeEvent(
                "Workplace Politics",
                "Office politics create a challenging environment.",
                EventPool.CAREER, -0.2,
                {"neuroticism": 0.1, "agreeableness": -0.1},
                {"power": -0.2, "security": -0.1},
                ["has_job"]
            ),
            LifeEvent(
                "Salary Increase",
                "Your performance is rewarded with a raise.",
                EventPool.CAREER, 0.4,
                {"self_esteem": 0.2, "competence": 0.1},
                {"achievement": 0.3, "security": 0.2},
                ["has_job"]
            ),
            LifeEvent(
                "Difficult Client",
                "A challenging client tests your patience and skills.",
                EventPool.CAREER, -0.1,
                {"neuroticism": 0.1, "agreeableness": -0.1},
                {"achievement": -0.1, "power": -0.1},
                ["has_job"]
            ),
            LifeEvent(
                "Team Leadership Role",
                "You're asked to lead a new team project.",
                EventPool.CAREER, 0.3,
                {"extraversion": 0.1, "achievement_striving": 0.2},
                {"power": 0.3, "achievement": 0.2},
                ["has_job"]
            ),
            LifeEvent(
                "Workplace Training",
                "You participate in valuable professional development.",
                EventPool.CAREER, 0.2,
                {"openness": 0.1, "conscientiousness": 0.1},
                {"achievement": 0.2, "security": 0.1},
                ["has_job"]
            ),
            LifeEvent(
                "Company Merger",
                "Your company merges with another, creating uncertainty.",
                EventPool.CAREER, -0.1,
                {"neuroticism": 0.2, "anxiety": 0.1},
                {"security": -0.2, "achievement": -0.1},
                ["has_job"]
            ),
            LifeEvent(
                "Freelance Opportunity",
                "A freelance project offers additional income and experience.",
                EventPool.CAREER, 0.2,
                {"openness": 0.1, "achievement_striving": 0.1},
                {"achievement": 0.2, "security": 0.1},
                []
            ),
            LifeEvent(
                "Workplace Friendship",
                "You form a meaningful friendship with a colleague.",
                EventPool.CAREER, 0.3,
                {"extraversion": 0.2, "agreeableness": 0.1},
                {"affiliation": 0.3, "security": 0.1},
                ["has_job"]
            ),
            LifeEvent(
                "Career Plateau",
                "You feel stuck in your current role with no advancement.",
                EventPool.CAREER, -0.2,
                {"neuroticism": 0.1, "frustration": 0.1},
                {"achievement": -0.2, "power": -0.1},
                ["has_job"]
            ),
            LifeEvent(
                "Industry Recognition",
                "Your work gets recognized by the broader industry.",
                EventPool.CAREER, 0.4,
                {"self_esteem": 0.3, "competence": 0.2},
                {"achievement": 0.4, "power": 0.2},
                ["has_job"]
            )
        ]
        
        # RELATIONSHIP EVENTS (30 events)
        events[EventPool.RELATIONSHIP] = [
            LifeEvent(
                "First Date",
                "You go on a first date with someone new.",
                EventPool.RELATIONSHIP, 0.2,
                {"extraversion": 0.2, "openness": 0.1},
                {"romance": 0.3, "affiliation": 0.2},
                []
            ),
            LifeEvent(
                "New Relationship",
                "You start a promising new romantic relationship.",
                EventPool.RELATIONSHIP, 0.4,
                {"extraversion": 0.2, "agreeableness": 0.1},
                {"romance": 0.5, "affiliation": 0.3},
                []
            ),
            LifeEvent(
                "Relationship Breakup",
                "Your romantic relationship comes to an end.",
                EventPool.RELATIONSHIP, -0.4,
                {"neuroticism": 0.3, "anxiety": 0.2},
                {"romance": -0.5, "affiliation": -0.2},
                ["in_relationship"]
            ),
            LifeEvent(
                "Marriage Proposal",
                "You decide to take your relationship to the next level.",
                EventPool.RELATIONSHIP, 0.5,
                {"commitment": 0.3, "agreeableness": 0.2},
                {"romance": 0.4, "security": 0.3},
                ["in_relationship"]
            ),
            LifeEvent(
                "Wedding Day",
                "You celebrate your marriage with friends and family.",
                EventPool.RELATIONSHIP, 0.6,
                {"extraversion": 0.3, "agreeableness": 0.2},
                {"romance": 0.5, "affiliation": 0.4},
                ["in_relationship"]
            ),
            LifeEvent(
                "Anniversary Celebration",
                "You celebrate another year together.",
                EventPool.RELATIONSHIP, 0.3,
                {"commitment": 0.2, "agreeableness": 0.1},
                {"romance": 0.3, "affiliation": 0.2},
                ["in_relationship"]
            ),
            LifeEvent(
                "Relationship Conflict",
                "A serious argument creates tension in your relationship.",
                EventPool.RELATIONSHIP, -0.3,
                {"neuroticism": 0.2, "agreeableness": -0.1},
                {"romance": -0.3, "security": -0.2},
                ["in_relationship"]
            ),
            LifeEvent(
                "Making Up",
                "You reconcile after a disagreement and grow closer.",
                EventPool.RELATIONSHIP, 0.2,
                {"agreeableness": 0.2, "commitment": 0.1},
                {"romance": 0.3, "affiliation": 0.2},
                ["in_relationship"]
            ),
            LifeEvent(
                "Meeting Parents",
                "You meet your partner's family for the first time.",
                EventPool.RELATIONSHIP, 0.1,
                {"anxiety": 0.1, "agreeableness": 0.1},
                {"romance": 0.1, "affiliation": 0.2},
                ["in_relationship"]
            ),
            LifeEvent(
                "Moving In Together",
                "You decide to share a home with your partner.",
                EventPool.RELATIONSHIP, 0.3,
                {"commitment": 0.3, "agreeableness": 0.1},
                {"romance": 0.3, "security": 0.2},
                ["in_relationship"]
            ),
            LifeEvent(
                "Long Distance Relationship",
                "Circumstances force you into a long-distance relationship.",
                EventPool.RELATIONSHIP, -0.2,
                {"neuroticism": 0.2, "anxiety": 0.1},
                {"romance": -0.2, "affiliation": -0.1},
                ["in_relationship"]
            ),
            LifeEvent(
                "Reconnecting with Ex",
                "You unexpectedly reconnect with a former partner.",
                EventPool.RELATIONSHIP, 0.0,
                {"nostalgia": 0.2, "conflict": 0.1},
                {"romance": 0.1, "stimulus": 0.2},
                []
            ),
            LifeEvent(
                "Jealousy Issues",
                "Jealousy creates strain in your relationship.",
                EventPool.RELATIONSHIP, -0.2,
                {"neuroticism": 0.2, "insecurity": 0.2},
                {"romance": -0.2, "security": -0.2},
                ["in_relationship"]
            ),
            LifeEvent(
                "Relationship Counseling",
                "You seek professional help for relationship issues.",
                EventPool.RELATIONSHIP, 0.1,
                {"openness": 0.2, "commitment": 0.1},
                {"romance": 0.1, "security": 0.1},
                ["in_relationship"]
            ),
            LifeEvent(
                "Surprise Romantic Gesture",
                "Your partner surprises you with something special.",
                EventPool.RELATIONSHIP, 0.4,
                {"extraversion": 0.1, "agreeableness": 0.2},
                {"romance": 0.4, "affiliation": 0.2},
                ["in_relationship"]
            ),
            LifeEvent(
                "Meeting Friends",
                "Your partner introduces you to their friend group.",
                EventPool.RELATIONSHIP, 0.2,
                {"extraversion": 0.2, "social": 0.1},
                {"affiliation": 0.3, "romance": 0.1},
                ["in_relationship"]
            ),
            LifeEvent(
                "Relationship Milestone",
                "You celebrate an important relationship milestone.",
                EventPool.RELATIONSHIP, 0.3,
                {"commitment": 0.2, "extraversion": 0.1},
                {"romance": 0.3, "affiliation": 0.2},
                ["in_relationship"]
            ),
            LifeEvent(
                "Different Life Goals",
                "You discover you and your partner want different things.",
                EventPool.RELATIONSHIP, -0.3,
                {"conflict": 0.2, "neuroticism": 0.1},
                {"romance": -0.3, "achievement": -0.1},
                ["in_relationship"]
            ),
            LifeEvent(
                "Vacation Together",
                "You take a romantic trip together.",
                EventPool.RELATIONSHIP, 0.4,
                {"extraversion": 0.2, "openness": 0.1},
                {"romance": 0.3, "stimulus": 0.3},
                ["in_relationship"]
            ),
            LifeEvent(
                "Meeting Someone Special",
                "You meet someone who could be 'the one'.",
                EventPool.RELATIONSHIP, 0.3,
                {"extraversion": 0.2, "openness": 0.2},
                {"romance": 0.4, "stimulus": 0.2},
                []
            ),
            LifeEvent(
                "Relationship Doubts",
                "You begin questioning your relationship's future.",
                EventPool.RELATIONSHIP, -0.2,
                {"neuroticism": 0.2, "anxiety": 0.1},
                {"romance": -0.2, "security": -0.2},
                ["in_relationship"]
            ),
            LifeEvent(
                "Partner's Success",
                "Your partner achieves something wonderful.",
                EventPool.RELATIONSHIP, 0.3,
                {"agreeableness": 0.2, "support": 0.1},
                {"affiliation": 0.3, "achievement": 0.1},
                ["in_relationship"]
            ),
            LifeEvent(
                "Shared Hobby",
                "You discover a hobby you both love.",
                EventPool.RELATIONSHIP, 0.2,
                {"openness": 0.1, "extraversion": 0.1},
                {"affiliation": 0.3, "stimulus": 0.1},
                ["in_relationship"]
            ),
            LifeEvent(
                "Financial Disagreement",
                "Money creates tension in your relationship.",
                EventPool.RELATIONSHIP, -0.2,
                {"conflict": 0.1, "neuroticism": 0.1},
                {"romance": -0.1, "security": -0.2},
                ["in_relationship"]
            ),
            LifeEvent(
                "Intimacy Issues",
                "Physical intimacy becomes challenging.",
                EventPool.RELATIONSHIP, -0.2,
                {"neuroticism": 0.2, "insecurity": 0.1},
                {"romance": -0.2, "affiliation": -0.1},
                ["in_relationship"]
            ),
            LifeEvent(
                "Future Planning",
                "You discuss future plans and goals together.",
                EventPool.RELATIONSHIP, 0.3,
                {"commitment": 0.3, "openness": 0.1},
                {"romance": 0.2, "security": 0.2},
                ["in_relationship"]
            ),
            LifeEvent(
                "Relationship Growth",
                "Your relationship evolves and deepens over time.",
                EventPool.RELATIONSHIP, 0.2,
                {"commitment": 0.2, "agreeableness": 0.1},
                {"romance": 0.3, "affiliation": 0.2},
                ["in_relationship"]
            ),
            LifeEvent(
                "Blended Family",
                "You navigate the complexities of a blended family.",
                EventPool.RELATIONSHIP, 0.1,
                {"patience": 0.2, "agreeableness": 0.1},
                {"affiliation": 0.2, "security": 0.1},
                ["in_relationship"]
            ),
            LifeEvent(
                "Renewed Romance",
                "You rediscover the spark in your long-term relationship.",
                EventPool.RELATIONSHIP, 0.4,
                {"extraversion": 0.2, "openness": 0.1},
                {"romance": 0.4, "stimulus": 0.2},
                ["in_relationship"]
            )
        ]
        
        # HEALTH EVENTS (25 events)
        events[EventPool.HEALTH] = [
            LifeEvent(
                "Fitness Journey Begins",
                "You decide to prioritize your physical health.",
                EventPool.HEALTH, 0.3,
                {"self_discipline": 0.2, "conscientiousness": 0.1},
                {"health": 0.4, "achievement": 0.2},
                []
            ),
            LifeEvent(
                "Health Scare",
                "A health issue reminds you to take care of yourself.",
                EventPool.HEALTH, -0.3,
                {"neuroticism": 0.3, "anxiety": 0.2},
                {"health": -0.3, "security": -0.2},
                []
            ),
            LifeEvent(
                "Regular Exercise Routine",
                "You establish a consistent exercise habit.",
                EventPool.HEALTH, 0.2,
                {"self_discipline": 0.3, "conscientiousness": 0.2},
                {"health": 0.3, "achievement": 0.2},
                []
            ),
            LifeEvent(
                "Healthy Diet Changes",
                "You improve your nutrition and eating habits.",
                EventPool.HEALTH, 0.2,
                {"self_discipline": 0.2, "conscientiousness": 0.1},
                {"health": 0.3, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Medical Checkup",
                "You attend a routine medical examination.",
                EventPool.HEALTH, 0.1,
                {"conscientiousness": 0.2, "responsibility": 0.1},
                {"health": 0.1, "security": 0.1},
                []
            ),
            LifeEvent(
                "Injury or Illness",
                "You suffer from an injury or illness that slows you down.",
                EventPool.HEALTH, -0.4,
                {"neuroticism": 0.2, "frustration": 0.1},
                {"health": -0.4, "achievement": -0.2},
                []
            ),
            LifeEvent(
                "Recovery Process",
                "You gradually recover and regain your strength.",
                EventPool.HEALTH, 0.2,
                {"patience": 0.2, "optimism": 0.1},
                {"health": 0.3, "achievement": 0.1},
                ["is_injured_or_sick"]
            ),
            LifeEvent(
                "Mental Health Awareness",
                "You recognize the importance of mental health.",
                EventPool.HEALTH, 0.2,
                {"openness": 0.2, "self_awareness": 0.2},
                {"health": 0.2, "security": 0.1},
                []
            ),
            LifeEvent(
                "Stress Management",
                "You develop healthy coping mechanisms for stress.",
                EventPool.HEALTH, 0.2,
                {"emotional_stability": 0.2, "self_discipline": 0.1},
                {"health": 0.2, "security": 0.2},
                []
            ),
            LifeEvent(
                "Sleep Issues",
                "Poor sleep affects your daily functioning.",
                EventPool.HEALTH, -0.2,
                {"neuroticism": 0.2, "fatigue": 0.2},
                {"health": -0.2, "achievement": -0.1},
                []
            ),
            LifeEvent(
                "Fitness Milestone",
                "You achieve a personal fitness goal.",
                EventPool.HEALTH, 0.4,
                {"self_esteem": 0.3, "competence": 0.2},
                {"health": 0.3, "achievement": 0.3},
                []
            ),
            LifeEvent(
                "Health Diagnosis",
                "You receive a specific medical diagnosis.",
                EventPool.HEALTH, -0.2,
                {"neuroticism": 0.2, "anxiety": 0.1},
                {"health": -0.2, "security": -0.2},
                []
            ),
            LifeEvent(
                "Treatment Plan",
                "You begin following a medical treatment plan.",
                EventPool.HEALTH, 0.1,
                {"conscientiousness": 0.2, "compliance": 0.2},
                {"health": 0.2, "security": 0.1},
                ["has_medical_condition"]
            ),
            LifeEvent(
                "Preventive Care",
                "You take proactive steps to maintain your health.",
                EventPool.HEALTH, 0.2,
                {"conscientiousness": 0.2, "responsibility": 0.1},
                {"health": 0.2, "security": 0.2},
                []
            ),
            LifeEvent(
                "Chronic Pain",
                "You begin dealing with chronic pain issues.",
                EventPool.HEALTH, -0.3,
                {"neuroticism": 0.2, "frustration": 0.2},
                {"health": -0.3, "achievement": -0.2},
                []
            ),
            LifeEvent(
                "Alternative Medicine",
                "You explore alternative health approaches.",
                EventPool.HEALTH, 0.1,
                {"openness": 0.2, "curiosity": 0.1},
                {"health": 0.1, "stimulus": 0.2},
                []
            ),
            LifeEvent(
                "Health Education",
                "You learn more about health and wellness.",
                EventPool.HEALTH, 0.2,
                {"openness": 0.2, "conscientiousness": 0.1},
                {"health": 0.2, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Support Group",
                "You join a health-related support group.",
                EventPool.HEALTH, 0.2,
                {"extraversion": 0.1, "support": 0.2},
                {"affiliation": 0.3, "health": 0.1},
                ["has_medical_condition"]
            ),
            LifeEvent(
                "Health Insurance Issues",
                "You face challenges with healthcare coverage.",
                EventPool.HEALTH, -0.2,
                {"frustration": 0.2, "stress": 0.1},
                {"security": -0.3, "health": -0.1},
                []
            ),
            LifeEvent(
                "Fitness Community",
                "You join a fitness community or gym.",
                EventPool.HEALTH, 0.2,
                {"extraversion": 0.2, "social": 0.1},
                {"affiliation": 0.2, "health": 0.2},
                []
            ),
            LifeEvent(
                "Health Technology",
                "You start using health tracking technology.",
                EventPool.HEALTH, 0.1,
                {"openness": 0.1, "conscientiousness": 0.1},
                {"health": 0.2, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Nutrition Education",
                "You learn about proper nutrition and meal planning.",
                EventPool.HEALTH, 0.2,
                {"conscientiousness": 0.2, "knowledge": 0.1},
                {"health": 0.2, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Mental Health Break",
                "You take time off for mental health recovery.",
                EventPool.HEALTH, 0.1,
                {"self_awareness": 0.2, "self_care": 0.2},
                {"health": 0.2, "security": 0.1},
                []
            ),
            LifeEvent(
                "Physical Therapy",
                "You undergo physical therapy for recovery.",
                EventPool.HEALTH, 0.1,
                {"patience": 0.2, "compliance": 0.2},
                {"health": 0.2, "achievement": 0.1},
                ["needs_physical_therapy"]
            ),
            LifeEvent(
                "Wellness Routine",
                "You establish a comprehensive wellness routine.",
                EventPool.HEALTH, 0.3,
                {"self_discipline": 0.3, "conscientiousness": 0.2},
                {"health": 0.3, "achievement": 0.2},
                []
            )
        ]
        
        # FINANCE EVENTS (25 events)
        events[EventPool.FINANCE] = [
            LifeEvent(
                "Financial Windfall",
                "You receive unexpected money or inheritance.",
                EventPool.FINANCE, 0.5,
                {"extraversion": 0.1, "optimism": 0.2},
                {"security": 0.4, "achievement": 0.2},
                []
            ),
            LifeEvent(
                "Financial Crisis",
                "You face serious financial difficulties.",
                EventPool.FINANCE, -0.5,
                {"neuroticism": 0.3, "stress": 0.2},
                {"security": -0.5, "achievement": -0.3},
                []
            ),
            LifeEvent(
                "New Investment",
                "You make a promising investment decision.",
                EventPool.FINANCE, 0.2,
                {"openness": 0.1, "risk_taking": 0.2},
                {"achievement": 0.2, "security": 0.1},
                []
            ),
            LifeEvent(
                "Investment Loss",
                "An investment performs poorly, causing losses.",
                EventPool.FINANCE, -0.3,
                {"neuroticism": 0.2, "regret": 0.1},
                {"security": -0.3, "achievement": -0.2},
                ["has_investments"]
            ),
            LifeEvent(
                "Budget Planning",
                "You create and commit to a financial budget.",
                EventPool.FINANCE, 0.2,
                {"conscientiousness": 0.3, "self_discipline": 0.2},
                {"security": 0.3, "achievement": 0.2},
                []
            ),
            LifeEvent(
                "Debt Payoff",
                "You successfully pay off significant debt.",
                EventPool.FINANCE, 0.4,
                {"self_discipline": 0.3, "relief": 0.2},
                {"security": 0.4, "achievement": 0.3},
                ["has_debt"]
            ),
            LifeEvent(
                "New Debt",
                "You take on new financial obligations.",
                EventPool.FINANCE, -0.1,
                {"caution": -0.1, "responsibility": 0.1},
                {"security": -0.2, "achievement": 0.0},
                []
            ),
            LifeEvent(
                "Salary Negotiation",
                "You successfully negotiate better compensation.",
                EventPool.FINANCE, 0.3,
                {"assertiveness": 0.2, "self_esteem": 0.1},
                {"achievement": 0.3, "security": 0.2},
                ["has_job"]
            ),
            LifeEvent(
                "Side Hustle Success",
                "Your side business or gig work becomes profitable.",
                EventPool.FINANCE, 0.3,
                {"entrepreneurship": 0.3, "achievement_striving": 0.2},
                {"achievement": 0.3, "security": 0.2},
                []
            ),
            LifeEvent(
                "Tax Issues",
                "You face complications with your taxes.",
                EventPool.FINANCE, -0.2,
                {"stress": 0.2, "frustration": 0.1},
                {"security": -0.2, "achievement": -0.1},
                []
            ),
            LifeEvent(
                "Financial Education",
                "You invest time in learning about personal finance.",
                EventPool.FINANCE, 0.2,
                {"openness": 0.2, "conscientiousness": 0.1},
                {"achievement": 0.2, "security": 0.1},
                []
            ),
            LifeEvent(
                "Emergency Fund",
                "You build an emergency savings fund.",
                EventPool.FINANCE, 0.3,
                {"responsibility": 0.3, "conscientiousness": 0.2},
                {"security": 0.4, "achievement": 0.2},
                []
            ),
            LifeEvent(
                "Major Purchase",
                "You make a significant purchase (home, car, etc.).",
                EventPool.FINANCE, 0.1,
                {"extraversion": 0.1, "achievement": 0.1},
                {"achievement": 0.2, "security": -0.1},
                []
            ),
            LifeEvent(
                "Financial Scam",
                "You fall victim to a financial scam.",
                EventPool.FINANCE, -0.3,
                {"trust": -0.2, "regret": 0.2},
                {"security": -0.3, "achievement": -0.2},
                []
            ),
            LifeEvent(
                "Retirement Planning",
                "You start seriously planning for retirement.",
                EventPool.FINANCE, 0.2,
                {"conscientiousness": 0.3, "responsibility": 0.2},
                {"security": 0.3, "achievement": 0.2},
                []
            ),
            LifeEvent(
                "Financial Arguments",
                "Money creates conflict in your relationships.",
                EventPool.FINANCE, -0.2,
                {"conflict": 0.2, "stress": 0.1},
                {"affiliation": -0.2, "security": -0.2},
                ["in_relationship"]
            ),
            LifeEvent(
                "Passive Income",
                "You establish a source of passive income.",
                EventPool.FINANCE, 0.3,
                {"entrepreneurship": 0.2, "achievement_striving": 0.1},
                {"achievement": 0.3, "security": 0.2},
                []
            ),
            LifeEvent(
                "Financial Windfall Loss",
                "You struggle to manage sudden wealth responsibly.",
                EventPool.FINANCE, -0.1,
                {"impulsivity": 0.1, "stress": 0.1},
                {"security": -0.1, "achievement": 0.0},
                ["has_sudden_wealth"]
            ),
            LifeEvent(
                "Credit Score Improvement",
                "You successfully improve your credit score.",
                EventPool.FINANCE, 0.2,
                {"responsibility": 0.2, "achievement_striving": 0.1},
                {"security": 0.2, "achievement": 0.2},
                []
            ),
            LifeEvent(
                "Financial Independence",
                "You achieve a level of financial independence.",
                EventPool.FINANCE, 0.5,
                {"self_esteem": 0.3, "freedom": 0.3},
                {"security": 0.5, "achievement": 0.4},
                []
            ),
            LifeEvent(
                "Business Venture",
                "You start your own business.",
                EventPool.FINANCE, 0.2,
                {"entrepreneurship": 0.4, "risk_taking": 0.2},
                {"achievement": 0.3, "security": -0.1},
                []
            ),
            LifeEvent(
                "Financial Setback",
                "Unexpected expenses create financial strain.",
                EventPool.FINANCE, -0.3,
                {"stress": 0.2, "anxiety": 0.1},
                {"security": -0.3, "achievement": -0.2},
                []
            ),
            LifeEvent(
                "Inheritance Planning",
                "You plan for managing potential inheritance.",
                EventPool.FINANCE, 0.1,
                {"responsibility": 0.2, "conscientiousness": 0.1},
                {"security": 0.2, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Financial Counseling",
                "You seek professional financial advice.",
                EventPool.FINANCE, 0.2,
                {"openness": 0.2, "responsibility": 0.1},
                {"security": 0.2, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Wealth Building",
                "You develop a long-term wealth building strategy.",
                EventPool.FINANCE, 0.3,
                {"conscientiousness": 0.3, "patience": 0.2},
                {"achievement": 0.3, "security": 0.3},
                []
            )
        ]
        
        # EDUCATION EVENTS (20 events)
        events[EventPool.EDUCATION] = [
            LifeEvent(
                "Enroll in Course",
                "You decide to pursue further education.",
                EventPool.EDUCATION, 0.2,
                {"openness": 0.3, "achievement_striving": 0.2},
                {"achievement": 0.3, "stimulus": 0.2},
                []
            ),
            LifeEvent(
                "Academic Achievement",
                "You excel in your studies and receive recognition.",
                EventPool.EDUCATION, 0.4,
                {"self_esteem": 0.3, "competence": 0.2},
                {"achievement": 0.4, "security": 0.1},
                ["is_student"]
            ),
            LifeEvent(
                "Academic Struggle",
                "You find your coursework challenging and overwhelming.",
                EventPool.EDUCATION, -0.2,
                {"neuroticism": 0.2, "frustration": 0.1},
                {"achievement": -0.2, "security": -0.1},
                ["is_student"]
            ),
            LifeEvent(
                "Graduation",
                "You successfully complete your program of study.",
                EventPool.EDUCATION, 0.5,
                {"self_esteem": 0.4, "competence": 0.3},
                {"achievement": 0.5, "security": 0.3},
                ["is_student"]
            ),
            LifeEvent(
                "Research Project",
                "You undertake an interesting research project.",
                EventPool.EDUCATION, 0.2,
                {"openness": 0.3, "curiosity": 0.2},
                {"achievement": 0.2, "stimulus": 0.3},
                ["is_student"]
            ),
            LifeEvent(
                "Study Group",
                "You form a study group with classmates.",
                EventPool.EDUCATION, 0.2,
                {"extraversion": 0.2, "cooperation": 0.2},
                {"affiliation": 0.3, "achievement": 0.1},
                ["is_student"]
            ),
            LifeEvent(
                "Scholarship Award",
                "You receive financial aid for your education.",
                EventPool.EDUCATION, 0.3,
                {"self_esteem": 0.2, "relief": 0.2},
                {"achievement": 0.3, "security": 0.3},
                ["is_student"]
            ),
            LifeEvent(
                "Academic Probation",
                "Your academic performance puts you on probation.",
                EventPool.EDUCATION, -0.3,
                {"anxiety": 0.2, "shame": 0.1},
                {"achievement": -0.3, "security": -0.2},
                ["is_student"]
            ),
            LifeEvent(
                "Change of Major",
                "You decide to switch your field of study.",
                EventPool.EDUCATION, 0.1,
                {"openness": 0.2, "uncertainty": 0.1},
                {"stimulus": 0.2, "achievement": 0.0},
                ["is_student"]
            ),
            LifeEvent(
                "Teaching Assistant",
                "You become a teaching assistant in your department.",
                EventPool.EDUCATION, 0.2,
                {"leadership": 0.2, "competence": 0.1},
                {"achievement": 0.2, "power": 0.1},
                ["is_student"]
            ),
            LifeEvent(
                "Academic Competition",
                "You participate in an academic competition.",
                EventPool.EDUCATION, 0.2,
                {"achievement_striving": 0.3, "competence": 0.1},
                {"achievement": 0.3, "stimulus": 0.2},
                ["is_student"]
            ),
            LifeEvent(
                "Study Abroad",
                "You study in a foreign country.",
                EventPool.EDUCATION, 0.3,
                {"openness": 0.4, "extraversion": 0.1},
                {"stimulus": 0.4, "achievement": 0.2},
                ["is_student"]
            ),
            LifeEvent(
                "Academic Mentor",
                "You find a mentor in your academic field.",
                EventPool.EDUCATION, 0.3,
                {"openness": 0.2, "cooperation": 0.1},
                {"achievement": 0.2, "affiliation": 0.2},
                ["is_student"]
            ),
            LifeEvent(
                "Final Exams",
                "You face the stress of final examinations.",
                EventPool.EDUCATION, -0.1,
                {"anxiety": 0.2, "stress": 0.1},
                {"achievement": -0.1, "security": -0.1},
                ["is_student"]
            ),
            LifeEvent(
                "Academic Publication",
                "You publish your research findings.",
                EventPool.EDUCATION, 0.4,
                {"self_esteem": 0.3, "competence": 0.2},
                {"achievement": 0.4, "power": 0.1},
                ["is_student"]
            ),
            LifeEvent(
                "Internship Opportunity",
                "You secure an internship related to your field.",
                EventPool.EDUCATION, 0.3,
                {"achievement_striving": 0.2, "openness": 0.1},
                {"achievement": 0.3, "security": 0.2},
                ["is_student"]
            ),
            LifeEvent(
                "Academic Conference",
                "You attend or present at an academic conference.",
                EventPool.EDUCATION, 0.2,
                {"extraversion": 0.2, "openness": 0.1},
                {"affiliation": 0.2, "achievement": 0.2},
                ["is_student"]
            ),
            LifeEvent(
                "Learning Disability",
                "You discover and work with a learning disability.",
                EventPool.EDUCATION, -0.2,
                {"frustration": 0.2, "determination": 0.1},
                {"achievement": -0.2, "security": -0.1},
                ["is_student"]
            ),
            LifeEvent(
                "Online Learning",
                "You adapt to online education platforms.",
                EventPool.EDUCATION, 0.1,
                {"adaptability": 0.2, "self_discipline": 0.1},
                {"achievement": 0.1, "stimulus": 0.1},
                ["is_student"]
            ),
            LifeEvent(
                "Academic Recognition",
                "Your academic achievements are formally recognized.",
                EventPool.EDUCATION, 0.4,
                {"self_esteem": 0.3, "pride": 0.2},
                {"achievement": 0.4, "power": 0.1},
                ["is_student"]
            )
        ]
        
        # SOCIAL EVENTS (25 events)
        events[EventPool.SOCIAL] = [
            LifeEvent(
                "New Friendship",
                "You form a meaningful new friendship.",
                EventPool.SOCIAL, 0.3,
                {"extraversion": 0.2, "agreeableness": 0.2},
                {"affiliation": 0.4, "stimulus": 0.1},
                []
            ),
            LifeEvent(
                "Social Gathering",
                "You attend a fun social event with friends.",
                EventPool.SOCIAL, 0.2,
                {"extraversion": 0.3, "sociability": 0.2},
                {"affiliation": 0.3, "stimulus": 0.2},
                []
            ),
            LifeEvent(
                "Friendship Conflict",
                "A disagreement creates tension with a friend.",
                EventPool.SOCIAL, -0.2,
                {"neuroticism": 0.1, "conflict": 0.1},
                {"affiliation": -0.3, "security": -0.1},
                []
            ),
            LifeEvent(
                "Social Anxiety",
                "You struggle with social anxiety in public situations.",
                EventPool.SOCIAL, -0.2,
                {"neuroticism": 0.3, "anxiety": 0.2},
                {"affiliation": -0.2, "security": -0.1},
                []
            ),
            LifeEvent(
                "Community Involvement",
                "You become active in your local community.",
                EventPool.SOCIAL, 0.3,
                {"extraversion": 0.2, "cooperation": 0.2},
                {"affiliation": 0.3, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Social Media Success",
                "Your social media presence gains positive attention.",
                EventPool.SOCIAL, 0.1,
                {"extraversion": 0.1, "validation": 0.1},
                {"affiliation": 0.2, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Loneliness",
                "You experience periods of loneliness and isolation.",
                EventPool.SOCIAL, -0.3,
                {"neuroticism": 0.2, "sadness": 0.2},
                {"affiliation": -0.3, "security": -0.2},
                []
            ),
            LifeEvent(
                "Group Project Success",
                "You successfully collaborate on a group project.",
                EventPool.SOCIAL, 0.3,
                {"cooperation": 0.3, "teamwork": 0.2},
                {"affiliation": 0.3, "achievement": 0.2},
                []
            ),
            LifeEvent(
                "Social Rejection",
                "You experience rejection in a social situation.",
                EventPool.SOCIAL, -0.3,
                {"neuroticism": 0.2, "hurt": 0.2},
                {"affiliation": -0.3, "security": -0.2},
                []
            ),
            LifeEvent(
                "Volunteer Work",
                "You dedicate time to helping others.",
                EventPool.SOCIAL, 0.3,
                {"empathy": 0.3, "altruism": 0.2},
                {"affiliation": 0.2, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Social Network Expansion",
                "Your social circle significantly expands.",
                EventPool.SOCIAL, 0.2,
                {"extraversion": 0.2, "openness": 0.1},
                {"affiliation": 0.3, "stimulus": 0.2},
                []
            ),
            LifeEvent(
                "Cultural Event",
                "You attend a cultural festival or celebration.",
                EventPool.SOCIAL, 0.2,
                {"openness": 0.3, "curiosity": 0.1},
                {"stimulus": 0.3, "affiliation": 0.1},
                []
            ),
            LifeEvent(
                "Social Misunderstanding",
                "A miscommunication causes social awkwardness.",
                EventPool.SOCIAL, -0.1,
                {"embarrassment": 0.1, "anxiety": 0.1},
                {"affiliation": -0.1, "security": -0.1},
                []
            ),
            LifeEvent(
                "Leadership Role",
                "You take on a leadership position in a group.",
                EventPool.SOCIAL, 0.3,
                {"leadership": 0.3, "responsibility": 0.2},
                {"power": 0.3, "achievement": 0.2},
                []
            ),
            LifeEvent(
                "Social Skills Development",
                "You actively work on improving your social skills.",
                EventPool.SOCIAL, 0.2,
                {"self_improvement": 0.3, "openness": 0.1},
                {"affiliation": 0.2, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Reconnecting with Friends",
                "You reconnect with old friends you've lost touch with.",
                EventPool.SOCIAL, 0.3,
                {"nostalgia": 0.2, "extraversion": 0.1},
                {"affiliation": 0.3, "stimulus": 0.1},
                []
            ),
            LifeEvent(
                "Social Media Drama",
                "Online conflicts create real-world stress.",
                EventPool.SOCIAL, -0.2,
                {"stress": 0.2, "frustration": 0.1},
                {"affiliation": -0.2, "security": -0.1},
                []
            ),
            LifeEvent(
                "Party Hosting",
                "You successfully host a social gathering.",
                EventPool.SOCIAL, 0.3,
                {"extraversion": 0.3, "hospitality": 0.2},
                {"affiliation": 0.3, "achievement": 0.2},
                []
            ),
            LifeEvent(
                "Social Comparison",
                "You find yourself comparing your life to others.",
                EventPool.SOCIAL, -0.1,
                {"envy": 0.1, "insecurity": 0.1},
                {"achievement": -0.1, "security": -0.1},
                []
            ),
            LifeEvent(
                "Club Membership",
                "You join a club or organization based on interests.",
                EventPool.SOCIAL, 0.2,
                {"extraversion": 0.2, "openness": 0.1},
                {"affiliation": 0.3, "stimulus": 0.2},
                []
            ),
            LifeEvent(
                "Social Support",
                "Friends rally around you during a difficult time.",
                EventPool.SOCIAL, 0.4,
                {"gratitude": 0.3, "comfort": 0.2},
                {"affiliation": 0.4, "security": 0.3},
                []
            ),
            LifeEvent(
                "Public Speaking",
                "You speak in front of a group and overcome nervousness.",
                EventPool.SOCIAL, 0.2,
                {"courage": 0.3, "self_esteem": 0.2},
                {"achievement": 0.3, "power": 0.1},
                []
            ),
            LifeEvent(
                "Social Media Detox",
                "You take a break from social media for mental health.",
                EventPool.SOCIAL, 0.1,
                {"self_care": 0.2, "mindfulness": 0.1},
                {"health": 0.1, "security": 0.1},
                []
            ),
            LifeEvent(
                "Networking Event",
                "You attend a professional networking event.",
                EventPool.SOCIAL, 0.2,
                {"extraversion": 0.3, "ambition": 0.1},
                {"affiliation": 0.2, "achievement": 0.2},
                []
            ),
            LifeEvent(
                "Social Boundary Setting",
                "You learn to set healthy boundaries in relationships.",
                EventPool.SOCIAL, 0.2,
                {"self_esteem": 0.2, "assertiveness": 0.2},
                {"affiliation": 0.1, "security": 0.2},
                []
            )
        ]
        
        # FAMILY EVENTS (25 events)
        events[EventPool.FAMILY] = [
            LifeEvent(
                "Family Celebration",
                "You gather with family for a joyous celebration.",
                EventPool.FAMILY, 0.4,
                {"extraversion": 0.2, "love": 0.3},
                {"affiliation": 0.4, "security": 0.3},
                []
            ),
            LifeEvent(
                "Family Conflict",
                "Tension and disagreement arise within the family.",
                EventPool.FAMILY, -0.3,
                {"conflict": 0.2, "stress": 0.1},
                {"affiliation": -0.3, "security": -0.2},
                []
            ),
            LifeEvent(
                "Family Illness",
                "A family member faces serious health challenges.",
                EventPool.FAMILY, -0.3,
                {"empathy": 0.2, "worry": 0.2},
                {"affiliation": -0.1, "security": -0.3},
                []
            ),
            LifeEvent(
                "Family Support",
                "Your family provides crucial support during difficulties.",
                EventPool.FAMILY, 0.4,
                {"gratitude": 0.3, "love": 0.2},
                {"affiliation": 0.4, "security": 0.3},
                []
            ),
            LifeEvent(
                "Family Reunion",
                "You reconnect with extended family members.",
                EventPool.FAMILY, 0.3,
                {"nostalgia": 0.2, "extraversion": 0.1},
                {"affiliation": 0.3, "stimulus": 0.2},
                []
            ),
            LifeEvent(
                "New Family Member",
                "A new baby or family member joins the family.",
                EventPool.FAMILY, 0.4,
                {"love": 0.3, "responsibility": 0.2},
                {"affiliation": 0.3, "security": 0.2},
                []
            ),
            LifeEvent(
                "Family Loss",
                "You experience the loss of a family member.",
                EventPool.FAMILY, -0.5,
                {"grief": 0.4, "sadness": 0.3},
                {"affiliation": -0.3, "security": -0.4},
                []
            ),
            LifeEvent(
                "Family Tradition",
                "You participate in a meaningful family tradition.",
                EventPool.FAMILY, 0.3,
                {"nostalgia": 0.2, "belonging": 0.2},
                {"affiliation": 0.3, "security": 0.2},
                []
            ),
            LifeEvent(
                "Parental Pride",
                "Your parents express pride in your accomplishments.",
                EventPool.FAMILY, 0.4,
                {"self_esteem": 0.3, "love": 0.2},
                {"achievement": 0.3, "affiliation": 0.3},
                []
            ),
            LifeEvent(
                "Family Expectations",
                "You feel pressure from family expectations.",
                EventPool.FAMILY, -0.2,
                {"stress": 0.2, "conflict": 0.1},
                {"achievement": -0.1, "security": -0.2},
                []
            ),
            LifeEvent(
                "Sibling Success",
                "A sibling achieves something wonderful.",
                EventPool.FAMILY, 0.2,
                {"pride": 0.2, "support": 0.1},
                {"affiliation": 0.2, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Family Financial Help",
                "You provide or receive financial help from family.",
                EventPool.FAMILY, 0.1,
                {"responsibility": 0.2, "gratitude": 0.1},
                {"security": 0.2, "affiliation": 0.1},
                []
            ),
            LifeEvent(
                "Family Vacation",
                "You take a vacation with family members.",
                EventPool.FAMILY, 0.3,
                {"extraversion": 0.2, "relaxation": 0.2},
                {"affiliation": 0.3, "stimulus": 0.2},
                []
            ),
            LifeEvent(
                "Family Secret",
                "You discover a surprising family secret.",
                EventPool.FAMILY, -0.1,
                {"shock": 0.2, "confusion": 0.1},
                {"stimulus": 0.2, "security": -0.1},
                []
            ),
            LifeEvent(
                "Caring for Parents",
                "You take on caregiving responsibilities for aging parents.",
                EventPool.FAMILY, 0.1,
                {"responsibility": 0.3, "love": 0.2},
                {"affiliation": 0.2, "security": 0.1},
                []
            ),
            LifeEvent(
                "Family Business",
                "You become involved in a family business.",
                EventPool.FAMILY, 0.2,
                {"entrepreneurship": 0.2, "cooperation": 0.1},
                {"achievement": 0.2, "affiliation": 0.2},
                []
            ),
            LifeEvent(
                "Family Disapproval",
                "Family members disapprove of your life choices.",
                EventPool.FAMILY, -0.2,
                {"conflict": 0.2, "hurt": 0.1},
                {"affiliation": -0.2, "security": -0.2},
                []
            ),
            LifeEvent(
                "Family Achievement",
                "The family celebrates a collective achievement.",
                EventPool.FAMILY, 0.3,
                {"pride": 0.2, "unity": 0.2},
                {"affiliation": 0.3, "achievement": 0.2},
                []
            ),
            LifeEvent(
                "Inheritance",
                "You receive an inheritance from a family member.",
                EventPool.FAMILY, 0.2,
                {"relief": 0.2, "responsibility": 0.1},
                {"security": 0.3, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Family Counseling",
                "The family seeks professional counseling.",
                EventPool.FAMILY, 0.1,
                {"openness": 0.2, "cooperation": 0.1},
                {"affiliation": 0.2, "security": 0.1},
                []
            ),
            LifeEvent(
                "Moving Away from Family",
                "You move to a new location away from family.",
                EventPool.FAMILY, -0.1,
                {"sadness": 0.2, "excitement": 0.1},
                {"affiliation": -0.2, "stimulus": 0.2},
                []
            ),
            LifeEvent(
                "Family Emergency",
                "A family emergency requires immediate attention.",
                EventPool.FAMILY, -0.3,
                {"worry": 0.3, "stress": 0.2},
                {"security": -0.3, "affiliation": -0.1},
                []
            ),
            LifeEvent(
                "Family Reconciliation",
                " estranged family members reconcile.",
                EventPool.FAMILY, 0.4,
                {"forgiveness": 0.3, "love": 0.2},
                {"affiliation": 0.4, "security": 0.3},
                []
            ),
            LifeEvent(
                "Family Holiday",
                "You celebrate a holiday with family traditions.",
                EventPool.FAMILY, 0.3,
                {"nostalgia": 0.2, "love": 0.2},
                {"affiliation": 0.3, "security": 0.2},
                []
            ),
            LifeEvent(
                "Family Advice",
                "You seek or receive important advice from family.",
                EventPool.FAMILY, 0.2,
                {"trust": 0.2, "gratitude": 0.1},
                {"security": 0.2, "achievement": 0.1},
                []
            )
        ]
        
        # PERSONAL GROWTH EVENTS (25 events)
        events[EventPool.PERSONAL_GROWTH] = [
            LifeEvent(
                "Self-Discovery Journey",
                "You begin a journey of self-discovery and personal growth.",
                EventPool.PERSONAL_GROWTH, 0.3,
                {"openness": 0.3, "self_awareness": 0.3},
                {"achievement": 0.2, "stimulus": 0.3},
                []
            ),
            LifeEvent(
                "Meditation Practice",
                "You establish a regular meditation or mindfulness practice.",
                EventPool.PERSONAL_GROWTH, 0.2,
                {"mindfulness": 0.3, "peace": 0.2},
                {"health": 0.2, "security": 0.2},
                []
            ),
            LifeEvent(
                "Therapy or Counseling",
                "You seek professional help for personal growth.",
                EventPool.PERSONAL_GROWTH, 0.2,
                {"openness": 0.3, "courage": 0.2},
                {"health": 0.2, "security": 0.2},
                []
            ),
            LifeEvent(
                "New Hobby",
                "You discover a new hobby that brings you joy.",
                EventPool.PERSONAL_GROWTH, 0.3,
                {"openness": 0.2, "creativity": 0.2},
                {"stimulus": 0.3, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Personal Breakthrough",
                "You have a major insight about yourself or life.",
                EventPool.PERSONAL_GROWTH, 0.4,
                {"self_awareness": 0.4, "clarity": 0.3},
                {"achievement": 0.3, "security": 0.2},
                []
            ),
            LifeEvent(
                "Overcoming Fear",
                "You successfully confront and overcome a significant fear.",
                EventPool.PERSONAL_GROWTH, 0.3,
                {"courage": 0.4, "self_esteem": 0.2},
                {"achievement": 0.3, "power": 0.2},
                []
            ),
            LifeEvent(
                "Life Philosophy Development",
                "You develop a personal philosophy or worldview.",
                EventPool.PERSONAL_GROWTH, 0.2,
                {"wisdom": 0.3, "clarity": 0.2},
                {"achievement": 0.2, "security": 0.1},
                []
            ),
            LifeEvent(
                "Creative Expression",
                "You find ways to express your creativity.",
                EventPool.PERSONAL_GROWTH, 0.2,
                {"creativity": 0.3, "self_expression": 0.2},
                {"stimulus": 0.3, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Personal Boundaries",
                "You learn to set and maintain healthy personal boundaries.",
                EventPool.PERSONAL_GROWTH, 0.3,
                {"self_esteem": 0.3, "assertiveness": 0.2},
                {"security": 0.3, "affiliation": 0.1},
                []
            ),
            LifeEvent(
                "Spiritual Exploration",
                "You explore spiritual or existential questions.",
                EventPool.PERSONAL_GROWTH, 0.2,
                {"openness": 0.3, "curiosity": 0.2},
                {"stimulus": 0.3, "security": 0.1},
                []
            ),
            LifeEvent(
                "Personal Challenge",
                "You set and achieve a challenging personal goal.",
                EventPool.PERSONAL_GROWTH, 0.3,
                {"determination": 0.3, "self_discipline": 0.2},
                {"achievement": 0.3, "self_esteem": 0.2},
                []
            ),
            LifeEvent(
                "Self-Acceptance",
                "You work on accepting yourself as you are.",
                EventPool.PERSONAL_GROWTH, 0.3,
                {"self_compassion": 0.4, "peace": 0.2},
                {"health": 0.2, "security": 0.2},
                []
            ),
            LifeEvent(
                "Learning from Mistakes",
                "You reflect on and learn from past mistakes.",
                EventPool.PERSONAL_GROWTH, 0.2,
                {"wisdom": 0.3, "humility": 0.2},
                {"achievement": 0.1, "security": 0.1},
                []
            ),
            LifeEvent(
                "Personal Values Clarification",
                "You identify and clarify your core personal values.",
                EventPool.PERSONAL_GROWTH, 0.3,
                {"clarity": 0.3, "authenticity": 0.2},
                {"achievement": 0.2, "security": 0.2},
                []
            ),
            LifeEvent(
                "Forgiveness Practice",
                "You practice forgiveness toward yourself and others.",
                EventPool.PERSONAL_GROWTH, 0.2,
                {"compassion": 0.3, "peace": 0.2},
                {"health": 0.2, "affiliation": 0.2},
                []
            ),
            LifeEvent(
                "Personal Retreat",
                "You take time for a personal retreat or sabbatical.",
                EventPool.PERSONAL_GROWTH, 0.2,
                {"reflection": 0.3, "peace": 0.2},
                {"health": 0.2, "stimulus": 0.2},
                []
            ),
            LifeEvent(
                "Skill Development",
                "You dedicate yourself to learning a new skill.",
                EventPool.PERSONAL_GROWTH, 0.2,
                {"growth": 0.3, "competence": 0.2},
                {"achievement": 0.2, "security": 0.1},
                []
            ),
            LifeEvent(
                "Life Purpose Discovery",
                "You gain clarity about your life purpose.",
                EventPool.PERSONAL_GROWTH, 0.4,
                {"purpose": 0.4, "clarity": 0.3},
                {"achievement": 0.3, "security": 0.2},
                []
            ),
            LifeEvent(
                "Emotional Intelligence Growth",
                "You develop greater emotional intelligence.",
                EventPool.PERSONAL_GROWTH, 0.3,
                {"emotional_awareness": 0.3, "empathy": 0.2},
                {"affiliation": 0.2, "achievement": 0.2},
                []
            ),
            LifeEvent(
                "Personal Reinvention",
                "You consciously reinvent aspects of yourself.",
                EventPool.PERSONAL_GROWTH, 0.2,
                {"transformation": 0.3, "courage": 0.2},
                {"stimulus": 0.3, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Mindfulness Integration",
                "You integrate mindfulness into daily life.",
                EventPool.PERSONAL_GROWTH, 0.2,
                {"presence": 0.3, "peace": 0.2},
                {"health": 0.2, "security": 0.2},
                []
            ),
            LifeEvent(
                "Personal Philosophy Shift",
                "Your fundamental worldview shifts significantly.",
                EventPool.PERSONAL_GROWTH, 0.3,
                {"transformation": 0.3, "wisdom": 0.2},
                {"stimulus": 0.3, "achievement": 0.2},
                []
            ),
            LifeEvent(
                "Self-Care Routine",
                "You establish a comprehensive self-care routine.",
                EventPool.PERSONAL_GROWTH, 0.2,
                {"self_compassion": 0.3, "responsibility": 0.2},
                {"health": 0.3, "security": 0.2},
                []
            ),
            LifeEvent(
                "Personal Legacy Planning",
                "You consider the legacy you want to leave.",
                EventPool.PERSONAL_GROWTH, 0.2,
                {"purpose": 0.3, "wisdom": 0.2},
                {"achievement": 0.2, "security": 0.1},
                []
            ),
            LifeEvent(
                "Authentic Living",
                "You commit to living more authentically.",
                EventPool.PERSONAL_GROWTH, 0.3,
                {"authenticity": 0.4, "courage": 0.2},
                {"achievement": 0.2, "security": 0.2},
                []
            )
        ]
        
        # UNEXPECTED EVENTS (25 events)
        events[EventPool.UNEXPECTED] = [
            LifeEvent(
                "Sudden Opportunity",
                "An unexpected opportunity appears out of nowhere.",
                EventPool.UNEXPECTED, 0.3,
                {"surprise": 0.3, "excitement": 0.2},
                {"stimulus": 0.4, "achievement": 0.2},
                []
            ),
            LifeEvent(
                "Unexpected Obstacle",
                "A sudden obstacle blocks your path forward.",
                EventPool.UNEXPECTED, -0.3,
                {"frustration": 0.3, "stress": 0.2},
                {"achievement": -0.3, "security": -0.2},
                []
            ),
            LifeEvent(
                "Chance Encounter",
                "A random meeting leads to significant consequences.",
                EventPool.UNEXPECTED, 0.2,
                {"serendipity": 0.3, "curiosity": 0.2},
                {"stimulus": 0.3, "affiliation": 0.2},
                []
            ),
            LifeEvent(
                "Weather Emergency",
                "Severe weather disrupts your plans.",
                EventPool.UNEXPECTED, -0.2,
                {"stress": 0.2, "adaptation": 0.1},
                {"security": -0.2, "achievement": -0.1},
                []
            ),
            LifeEvent(
                "Found Money",
                "You unexpectedly find money or valuables.",
                EventPool.UNEXPECTED, 0.3,
                {"surprise": 0.3, "relief": 0.2},
                {"security": 0.3, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Lost Item",
                "You lose something important unexpectedly.",
                EventPool.UNEXPECTED, -0.2,
                {"frustration": 0.2, "stress": 0.1},
                {"security": -0.2, "achievement": -0.1},
                []
            ),
            LifeEvent(
                "Sudden Inspiration",
                "A flash of inspiration strikes at an unexpected moment.",
                EventPool.UNEXPECTED, 0.3,
                {"creativity": 0.4, "excitement": 0.2},
                {"stimulus": 0.3, "achievement": 0.2},
                []
            ),
            LifeEvent(
                "Random Act of Kindness",
                "A stranger shows you unexpected kindness.",
                EventPool.UNEXPECTED, 0.3,
                {"gratitude": 0.4, "surprise": 0.2},
                {"affiliation": 0.3, "security": 0.1},
                []
            ),
            LifeEvent(
                "System Failure",
                "Important technology or systems fail unexpectedly.",
                EventPool.UNEXPECTED, -0.2,
                {"frustration": 0.2, "adaptation": 0.1},
                {"security": -0.2, "achievement": -0.1},
                []
            ),
            LifeEvent(
                "Unexpected News",
                "You receive surprising news that changes everything.",
                EventPool.UNEXPECTED, 0.1,
                {"shock": 0.3, "confusion": 0.2},
                {"stimulus": 0.3, "security": -0.1},
                []
            ),
            LifeEvent(
                "Spontaneous Trip",
                "You decide to take an impromptu trip.",
                EventPool.UNEXPECTED, 0.3,
                {"spontaneity": 0.4, "excitement": 0.2},
                {"stimulus": 0.4, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Unexpected Guest",
                "Someone shows up at your door unexpectedly.",
                EventPool.UNEXPECTED, 0.1,
                {"surprise": 0.2, "adaptation": 0.1},
                {"stimulus": 0.2, "affiliation": 0.1},
                []
            ),
            LifeEvent(
                "Sudden Realization",
                "You suddenly understand something important.",
                EventPool.UNEXPECTED, 0.3,
                {"insight": 0.4, "clarity": 0.2},
                {"achievement": 0.2, "stimulus": 0.2},
                []
            ),
            LifeEvent(
                "Unexpected Compliment",
                "A stranger gives you a meaningful compliment.",
                EventPool.UNEXPECTED, 0.2,
                {"surprise": 0.2, "self_esteem": 0.2},
                {"affiliation": 0.2, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Schedule Disruption",
                "Your plans are suddenly disrupted by external events.",
                EventPool.UNEXPECTED, -0.1,
                {"frustration": 0.2, "flexibility": 0.1},
                {"achievement": -0.1, "security": -0.1},
                []
            ),
            LifeEvent(
                "Unexpected Discovery",
                "You discover something surprising by accident.",
                EventPool.UNEXPECTED, 0.2,
                {"curiosity": 0.3, "surprise": 0.2},
                {"stimulus": 0.3, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Power Outage",
                "A power outage forces you to adapt your plans.",
                EventPool.UNEXPECTED, -0.1,
                {"adaptation": 0.2, "frustration": 0.1},
                {"security": -0.1, "achievement": -0.1},
                []
            ),
            LifeEvent(
                "Unexpected Invitation",
                "You receive an unexpected invitation to something special.",
                EventPool.UNEXPECTED, 0.2,
                {"excitement": 0.3, "curiosity": 0.2},
                {"stimulus": 0.3, "affiliation": 0.2},
                []
            ),
            LifeEvent(
                "Traffic Jam",
                "An unexpected traffic jam makes you late.",
                EventPool.UNEXPECTED, -0.1,
                {"frustration": 0.2, "stress": 0.1},
                {"achievement": -0.1, "security": -0.1},
                []
            ),
            LifeEvent(
                "Unexpected Connection",
                "You discover an unexpected connection to someone.",
                EventPool.UNEXPECTED, 0.2,
                {"surprise": 0.3, "curiosity": 0.2},
                {"affiliation": 0.3, "stimulus": 0.2},
                []
            ),
            LifeEvent(
                "Sudden Change of Plans",
                "You must suddenly change your plans due to circumstances.",
                EventPool.UNEXPECTED, -0.1,
                {"adaptation": 0.2, "frustration": 0.1},
                {"achievement": -0.1, "security": -0.1},
                []
            ),
            LifeEvent(
                "Unexpected Gift",
                "Someone gives you an unexpected, thoughtful gift.",
                EventPool.UNEXPECTED, 0.3,
                {"gratitude": 0.3, "surprise": 0.2},
                {"affiliation": 0.3, "security": 0.1},
                []
            ),
            LifeEvent(
                "Sudden Memory",
                "A forgotten memory suddenly returns with clarity.",
                EventPool.UNEXPECTED, 0.2,
                {"nostalgia": 0.3, "insight": 0.2},
                {"stimulus": 0.2, "achievement": 0.1},
                []
            ),
            LifeEvent(
                "Unexpected Challenge",
                "You face an unforeseen challenge that tests your abilities.",
                EventPool.UNEXPECTED, -0.2,
                {"determination": 0.2, "stress": 0.1},
                {"achievement": 0.1, "security": -0.2},
                []
            ),
            LifeEvent(
                "Serendipitous Moment",
                "Perfect timing leads to a fortunate coincidence.",
                EventPool.UNEXPECTED, 0.3,
                {"serendipity": 0.4, "gratitude": 0.2},
                {"stimulus": 0.3, "achievement": 0.2},
                []
            )
        ]
        
        return events
    
    def select_event(self, character_state: Dict, pool_weights: Optional[Dict[EventPool, float]] = None) -> Optional[LifeEvent]:
        """Select an appropriate event based on character state and pool weights"""
        if pool_weights is None:
            pool_weights = {pool: 1.0 for pool in EventPool}
        
        # Filter events that can trigger
        available_events = []
        for pool, events_list in self.events.items():
            pool_weight = pool_weights.get(pool, 1.0)
            for event in events_list:
                if event.can_trigger(character_state):
                    # Avoid recent events (simple time-based cooldown)
                    if event.title not in [e.title for e in self.recent_events[-5:]]:
                        available_events.append((event, pool_weight))
        
        if not available_events:
            return None
        
        # Weighted random selection
        events_with_weights = [(event, weight) for event, weight in available_events]
        total_weight = sum(weight for _, weight in events_with_weights)
        
        if total_weight == 0:
            return None
        
        rand = random.uniform(0, total_weight)
        current_weight = 0
        
        for event, weight in events_with_weights:
            current_weight += weight
            if rand <= current_weight:
                self.recent_events.append(event)
                return event
        
        return None
    
    def get_pool_stats(self) -> Dict[str, int]:
        """Get statistics about events in each pool"""
        return {pool.value: len(events) for pool, events in self.events.items()}
