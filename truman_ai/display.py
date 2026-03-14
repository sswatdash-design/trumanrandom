"""
TRUMAN AI Display System
Terminal UI for visualizing character state and simulation

[SF] Clean terminal interface and visualization
[AC] Atomic functions for UI rendering and updates
"""

import os
import sys
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
from .config import CHARACTER_NAME, WEATHER_STATES

class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

class ProgressBar:
    """Renders progress bars for visualizing levels"""
    
    @staticmethod
    def render(value: float, max_value: float = 1.0, width: int = 20,
               color: str = Colors.GREEN, show_percentage: bool = True) -> str:
        """Render a progress bar"""
        if max_value == 0:
            filled = 0
        else:
            filled = int((value / max_value) * width)
        
        bar = '█' * filled + '░' * (width - filled)
        
        if show_percentage:
            percentage = (value / max_value) * 100 if max_value > 0 else 0
            return f"{color}[{bar}]{Colors.RESET} {percentage:5.1f}%"
        else:
            return f"{color}[{bar}]{Colors.RESET}"
    
    @staticmethod
    def render_mood_bar(mood_value: float, width: int = 30) -> str:
        """Render a mood bar with color coding"""
        if mood_value > 0.7:
            color = Colors.GREEN
        elif mood_value > 0.5:
            color = Colors.CYAN
        elif mood_value > 0.3:
            color = Colors.YELLOW
        else:
            color = Colors.RED
        
        return ProgressBar.render(mood_value, 1.0, width, color, False)

class Display:
    """Main display system for the Truman AI"""
    
    def __init__(self, character_name: str = CHARACTER_NAME):
        self.character_name = character_name
        self.terminal_width = 80
        self.terminal_height = 24
        self.clear_screen()
        
    def clear_screen(self) -> None:
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def get_terminal_size(self) -> tuple:
        """Get current terminal size"""
        try:
            size = os.get_terminal_size()
            return (size.columns, size.lines)
        except:
            return (80, 24)
    
    def render_header(self, current_time: datetime, location: str,
                     weather: str) -> None:
        """Render the header with basic info"""
        self.terminal_width, _ = self.get_terminal_size()
        
        # Character name and title
        title = f"{Colors.BOLD}{Colors.CYAN}═══ {self.character_name} AI Simulation ═══{Colors.RESET}"
        print(title.center(self.terminal_width))
        
        # Time, location, weather info
        time_str = current_time.strftime("%Y-%m-%d %H:%M")
        info_line = f"Time: {Colors.YELLOW}{time_str}{Colors.RESET} | "
        info_line += f"Location: {Colors.GREEN}{location}{Colors.RESET} | "
        info_line += f"Weather: {Colors.BLUE}{weather}{Colors.RESET}"
        
        print(info_line.center(self.terminal_width))
        print("─" * self.terminal_width)
    
    def render_mood_section(self, mood_engine) -> None:
        """Render the mood and emotional state section"""
        print(f"\n{Colors.BOLD}🧠 MOOD & EMOTIONS{Colors.RESET}")
        print("┌" + "─" * 78 + "┐")
        
        # Overall mood
        mood_desc = mood_engine.get_mood_description()
        mood_value = mood_engine.current_mood
        mood_bar = ProgressBar.render_mood_bar(mood_value, 25)
        
        print(f"│ Overall Mood: {Colors.BOLD}{mood_desc:<15}{Colors.RESET} {mood_bar:<35} │")
        
        # Emotional state
        emotions = mood_engine.emotional_state
        emotion_line = "│ Emotions:     "
        for emotion, value in emotions.items():
            if value > 0.1:
                color = Colors.GREEN if emotion == "happiness" else Colors.RED
                emotion_line += f"{color}{emotion}:{value:.2f} {Colors.RESET}"
        
        print(emotion_line.ljust(79) + "│")
        
        # Mood trend
        trend = mood_engine.get_mood_trend()
        trend_color = Colors.GREEN if trend == "Improving" else Colors.RED if trend == "Declining" else Colors.YELLOW
        print(f"│ Trend:         {trend_color}{trend}{Colors.RESET}".ljust(79) + "│")
        
        print("└" + "─" * 78 + "┘")
    
    def render_drives_section(self, mood_engine) -> None:
        """Render the biological drives section"""
        print(f"\n{Colors.BOLD}🎯 BIOLOGICAL DRIVES{Colors.RESET}")
        print("┌" + "─" * 78 + "┐")
        
        drives_status = mood_engine.get_drive_status()
        
        for drive_name, status in list(drives_status.items())[:8]:  # Show top 8 drives
            drive_level = mood_engine.drives[drive_name].current_level
            bar_color = Colors.GREEN if drive_level > 0.6 else Colors.YELLOW if drive_level > 0.3 else Colors.RED
            
            # Truncate long drive names
            display_name = drive_name[:12].ljust(12)
            status_display = status[:15].ljust(15)
            
            bar = ProgressBar.render(drive_level, 1.0, 20, bar_color, False)
            print(f"│ {display_name} {status_display} {bar:<25} │")
        
        print("└" + "─" * 78 + "┘")
    
    def render_personality_section(self, mood_engine) -> None:
        """Render the personality traits section"""
        print(f"\n{Colors.BOLD}👤 PERSONALITY TRAITS{Colors.RESET}")
        print("┌" + "─" * 78 + "┐")
        
        traits = mood_engine.personality.get_dominant_traits(5)
        
        for trait_name, trait_value in traits:
            # Color code based on trait level
            if trait_value > 0.7:
                color = Colors.GREEN
            elif trait_value > 0.4:
                color = Colors.YELLOW
            else:
                color = Colors.RED
            
            display_name = trait_name.replace("_", " ").title().ljust(15)
            bar = ProgressBar.render(trait_value, 1.0, 15, color, False)
            
            print(f"│ {display_name} {bar:<25} {trait_value:.2f}".ljust(79) + "│")
        
        print("└" + "─" * 78 + "┘")
    
    def render_memory_section(self, memory_system) -> None:
        """Render the memory system overview"""
        print(f"\n{Colors.BOLD}🧠 MEMORY SYSTEM{Colors.RESET}")
        print("┌" + "─" * 78 + "┐")
        
        summary = memory_system.get_memory_summary()
        
        print(f"│ Working Memory:  {summary['working_memory_count']:>3} items".ljust(79) + "│")
        print(f"│ Episodic Memory: {summary['episodic_memory_count']:>3} items".ljust(79) + "│")
        print(f"│ Semantic Memory: {summary['semantic_memory_count']:>3} facts".ljust(79) + "│")
        print(f"│ Concepts:        {summary['concepts_count']:>3} concepts".ljust(79) + "│")
        
        print("└" + "─" * 78 + "┘")
    
    def render_recent_events_section(self, events: List[Dict]) -> None:
        """Render recent life events"""
        print(f"\n{Colors.BOLD}📅 RECENT EVENTS{Colors.RESET}")
        print("┌" + "─" * 78 + "┐")
        
        if not events:
            print(f"│ {'No recent events':^77} │")
        else:
            for event in events[-5:]:  # Show last 5 events
                title = event.get('title', 'Unknown Event')[:40]
                impact = event.get('mood_impact', 0.0)
                
                # Color code by impact
                if impact > 0.2:
                    color = Colors.GREEN
                    impact_symbol = "😊"
                elif impact < -0.2:
                    color = Colors.RED
                    impact_symbol = "😢"
                else:
                    color = Colors.YELLOW
                    impact_symbol = "😐"
                
                event_line = f"│ {impact_symbol} {color}{title:<40}{Colors.RESET} "
                event_line += f"Impact: {impact:+.2f}".ljust(35)
                print(event_line + "│")
        
        print("└" + "─" * 78 + "┘")
    
    def render_thoughts_section(self, brain) -> None:
        """Render recent thoughts and cognitive state"""
        print(f"\n{Colors.BOLD}💭 COGNITIVE STATE{Colors.RESET}")
        print("┌" + "─" * 78 + "┐")
        
        cognitive_state = brain.get_cognitive_state()
        current_focus = cognitive_state.get('current_focus', 'No current focus')
        
        print(f"│ Current Focus: {current_focus[:50]:<50}".ljust(79) + "│")
        print(f"│ Thought Count: {cognitive_state['thought_count']:>3} | "
              f"Conversation Length: {cognitive_state['conversation_length']:>3}".ljust(79) + "│")
        
        recent_thoughts = cognitive_state.get('recent_thoughts', [])
        if recent_thoughts:
            print("│ Recent Thoughts:                                               │")
            for thought in recent_thoughts[-3:]:  # Show last 3 thoughts
                thought_text = thought[:70].ljust(70)
                print(f"│ • {thought_text} │")
        
        print("└" + "─" * 78 + "┘")
    
    def render_activity_log(self, activities: List[str]) -> None:
        """Render recent activity log"""
        print(f"\n{Colors.BOLD}📝 ACTIVITY LOG{Colors.RESET}")
        print("┌" + "─" * 78 + "┐")
        
        if not activities:
            print(f"│ {'No recent activities':^77} │")
        else:
            for activity in activities[-8:]:  # Show last 8 activities
                # Truncate long activities
                display_activity = activity[:70].ljust(70)
                print(f"│ {display_activity} │")
        
        print("└" + "─" * 78 + "┘")
    
    def render_status_bar(self, simulation_speed: float, fps: float) -> None:
        """Render status bar at the bottom"""
        print("\n" + "─" * self.terminal_width)
        
        status_items = [
            f"Speed: {simulation_speed}x",
            f"FPS: {fps:.1f}",
            f"Terminal: {self.terminal_width}x{self.terminal_height}",
            f"Updated: {datetime.now().strftime('%H:%M:%S')}"
        ]
        
        status_line = " | ".join(status_items)
        print(f"{Colors.CYAN}{status_line.center(self.terminal_width)}{Colors.RESET}")
    
    def render_full_display(self, current_time: datetime, location: str, weather: str,
                           mood_engine, memory_system, brain, events: List[Dict],
                           activities: List[str], simulation_speed: float = 1.0,
                           fps: float = 30.0) -> None:
        """Render the complete display"""
        self.clear_screen()
        
        # Update terminal size
        self.terminal_width, self.terminal_height = self.get_terminal_size()
        
        # Render all sections
        self.render_header(current_time, location, weather)
        self.render_mood_section(mood_engine)
        self.render_drives_section(mood_engine)
        self.render_personality_section(mood_engine)
        self.render_memory_section(memory_system)
        self.render_recent_events_section(events)
        self.render_thoughts_section(brain)
        self.render_activity_log(activities)
        self.render_status_bar(simulation_speed, fps)
    
    def render_simple_status(self, mood_engine, current_time: datetime) -> None:
        """Render a simple status line"""
        mood_desc = mood_engine.get_mood_description()
        mood_value = mood_engine.current_mood
        time_str = current_time.strftime("%H:%M:%S")
        
        status = f"[{time_str}] {self.character_name} - {mood_desc} ({mood_value:.2f})"
        print(f"{Colors.CYAN}{status}{Colors.RESET}")
    
    def render_event_notification(self, event_title: str, event_description: str,
                                 mood_impact: float) -> None:
        """Render a notification for a new event"""
        if mood_impact > 0.2:
            color = Colors.GREEN
            symbol = "🎉"
        elif mood_impact < -0.2:
            color = Colors.RED
            symbol = "⚠️"
        else:
            color = Colors.YELLOW
            symbol = "📢"
        
        print(f"\n{color}{symbol} EVENT: {event_title}{Colors.RESET}")
        print(f"{color}{event_description}{Colors.RESET}")
        print(f"{color}Mood Impact: {mood_impact:+.2f}{Colors.RESET}")
        print("─" * 50)
    
    def render_decision_prompt(self, options: List[str], situation: str) -> None:
        """Render a decision prompt"""
        print(f"\n{Colors.BOLD}{Colors.YELLOW}🤔 DECISION REQUIRED{Colors.RESET}")
        print(f"Situation: {situation}")
        print("\nOptions:")
        
        for i, option in enumerate(options):
            print(f"{Colors.CYAN}{i+1}.{Colors.RESET} {option}")
        
        print(f"\n{Colors.GREEN}Choose an option (1-{len(options)}):{Colors.RESET}", end=" ")
    
    def render_reflection_display(self, experience: str, reflection: str) -> None:
        """Display a reflection"""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}🤔 REFLECTION{Colors.RESET}")
        print(f"Experience: {experience}")
        print(f"\n{Colors.CYAN}Reflection:{Colors.RESET}")
        print(reflection)
        print("─" * 50)
    
    def render_error_message(self, error: str) -> None:
        """Render an error message"""
        print(f"{Colors.RED}{Colors.BOLD}ERROR: {error}{Colors.RESET}")
    
    def render_success_message(self, message: str) -> None:
        """Render a success message"""
        print(f"{Colors.GREEN}{Colors.BOLD}SUCCESS: {message}{Colors.RESET}")
    
    def render_info_message(self, message: str) -> None:
        """Render an info message"""
        print(f"{Colors.BLUE}{Colors.BOLD}INFO: {message}{Colors.RESET}")
    
    def get_user_input(self, prompt: str = "") -> str:
        """Get user input with optional prompt"""
        if prompt:
            print(f"{Colors.CYAN}{prompt}{Colors.RESET}", end=" ")
        
        try:
            return input().strip()
        except KeyboardInterrupt:
            return ""
    
    def confirm_action(self, message: str) -> bool:
        """Get user confirmation"""
        response = self.get_user_input(f"{message} (y/n): ").lower()
        return response in ['y', 'yes', '']
    
    def render_menu(self, title: str, options: List[str]) -> int:
        """Render a menu and get selection"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}═ {title} ═{Colors.RESET}")
        
        for i, option in enumerate(options):
            print(f"{Colors.YELLOW}{i+1}.{Colors.RESET} {option}")
        
        print(f"{Colors.YELLOW}0.{Colors.RESET} Exit")
        
        while True:
            try:
                choice = self.get_user_input("Enter your choice: ")
                choice_num = int(choice)
                if 0 <= choice_num <= len(options):
                    return choice_num
                else:
                    self.render_error_message("Invalid choice. Please try again.")
            except ValueError:
                self.render_error_message("Please enter a valid number.")
    
    def render_help_screen(self) -> None:
        """Render help information"""
        help_text = f"""
{Colors.BOLD}{Colors.CYAN}TRUMAN AI - HELP{Colors.RESET}

{Colors.YELLOW}Controls:{Colors.RESET}
• The simulation runs automatically
• Press Ctrl+C to exit
• The display updates in real-time

{Colors.YELLOW}Display Sections:{Colors.RESET}
• Mood & Emotions: Current emotional state
• Biological Drives: Basic needs and motivations
• Personality Traits: Character personality expression
• Memory System: Overview of memory storage
• Recent Events: Latest life events
• Cognitive State: Current thoughts and focus
• Activity Log: Recent actions and experiences

{Colors.YELLOW}Mood Colors:{Colors.RESET}
{Colors.GREEN}Green{Colors.RESET}: Positive mood (>0.7)
{Colors.CYAN}Cyan{Colors.RESET}: Good mood (0.5-0.7)
{Colors.YELLOW}Yellow{Colors.RESET}: Neutral mood (0.3-0.5)
{Colors.RED}Red{Colors.RESET}: Low mood (<0.3)

{Colors.YELLOW}Drive Levels:{Colors.RESET}
{Colors.GREEN}Green{Colors.RESET}: Well satisfied (>60%)
{Colors.YELLOW}Yellow{Colors.RESET}: Moderate (30-60%)
{Colors.RED}Red{Colors.RESET}: Needs attention (<30%)

Press any key to continue...
"""
        
        print(help_text)
        self.get_user_input()

class DisplayManager:
    """Manages display updates and rendering coordination"""
    
    def __init__(self, character_name: str = CHARACTER_NAME):
        self.display = Display(character_name)
        self.last_update = time.time()
        self.update_interval = 1.0  # Update every second
        self.frame_count = 0
        self.start_time = time.time()
        
    def should_update(self) -> bool:
        """Check if display should update"""
        current_time = time.time()
        return current_time - self.last_update >= self.update_interval
    
    def update_display(self, current_time: datetime, location: str, weather: str,
                      mood_engine, memory_system, brain, events: List[Dict],
                      activities: List[str], simulation_speed: float = 1.0) -> None:
        """Update the display if needed"""
        if self.should_update():
            # Calculate FPS
            self.frame_count += 1
            elapsed = time.time() - self.start_time
            fps = self.frame_count / elapsed if elapsed > 0 else 0
            
            # Render full display
            self.display.render_full_display(
                current_time, location, weather, mood_engine, memory_system,
                brain, events, activities, simulation_speed, fps
            )
            
            self.last_update = time.time()
    
    def force_update(self, current_time: datetime, location: str, weather: str,
                    mood_engine, memory_system, brain, events: List[Dict],
                    activities: List[str], simulation_speed: float = 1.0) -> None:
        """Force an immediate display update"""
        self.frame_count += 1
        elapsed = time.time() - self.start_time
        fps = self.frame_count / elapsed if elapsed > 0 else 0
        
        self.display.render_full_display(
            current_time, location, weather, mood_engine, memory_system,
            brain, events, activities, simulation_speed, fps
        )
        
        self.last_update = time.time()
    
    def get_fps(self) -> float:
        """Get current FPS"""
        elapsed = time.time() - self.start_time
        return self.frame_count / elapsed if elapsed > 0 else 0
