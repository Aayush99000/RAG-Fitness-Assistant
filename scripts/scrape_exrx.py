import requests
from bs4 import BeautifulSoup
import json
import os
import time
from typing import List, Dict
import re

class ExRxScrapper:
    def __init__(self):
        self.base_url = "https://exrx.net/robots.txt"
        self.headers = {
            'User-Agent':  'Mozilla/5.0 (Educational Project) AppleWebKit/537.36'
        }
        self.exercises =[]

    def fetch_page(self, url: str) -> str:
        """Fetch and parse a webpape"""
        print(f"Fetching URL: {url}")
        time.sleep(1)  # Be respectful to the server

        try:
            response =requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
        
    def get_muscle_groups(self) -> List[Dict[str, str]]:
        """Get all muscle groups from the main page"""
        url = f"{self.base_url}/Lists/Directory"
        soup = self.fetch_page(url)
        if not soup:
            return {}
        muscle_groups = []

        #Find all muscle group links 
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text(strip =True)
            
            #Look for muscle list page

            if '/Lists/' in href and 'ExList' not in href:
                full_url = f"{self.base_url}{href}" if href.startswith('/') else href
                muscle_groups[text] = full_url

        print(f"Found {len(muscle_groups)} muscle groups.")
        return muscle_groups
    
    def get_exercises_from_muscle_group(self, url: str , category: str) -> List[Dict] :
        """Get all exercises from a muscle group page"""
        soup = self.get_page(url)

        if not soup:
            return []
        exercises = []
        #Find exercises links
        for link in soup.find_all('a', href=True):
            href = link['href']

            #Exercise pages are typyically under /weightExercises/ or /Polymetrics/
            if any(x in href for x in ['/WeightExercises/', '/Plyometrics/', '/Stretches/']):
                exercise_url = f"{self.base_url}{href}" if href.startswith('/') else href
                exercise_name = link.get_text(strip=True)
                
                if exercise_name:  # Skip empty links
                    exercise_data = self.scrape_exercise_page(exercise_url, exercise_name, category)
                    if exercise_data:
                        exercises.append(exercise_data)
        
        return exercises
    
    def scrape_exercise_page(self,uurl:str , name:str,category:str) ->Dict:
        """Scrape individual exercise page"""
        soup = self.get_page(url)
        
        if not soup:
            return None
        
        exercise = {
            'name': name,
            'category': category,
            'url': url,
            'muscle_groups': [],
            'equipment': 'Unknown',
            'difficulty': 'Intermediate',
            'instructions': '',
            'form_tips': ''
        }
        
        # Extract content from the page
        # ExRx typically has content in paragraph tags
        
        # Get all text content
        content_divs = soup.find_all(['p', 'div', 'li'])
        
        instructions = []
        muscles = []
        
        for element in content_divs:
            text = element.get_text(strip=True)
            
            # Look for muscle information
            if 'Target:' in text or 'target' in text.lower():
                # Extract muscle names
                muscle_match = re.findall(r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)', text)
                muscles.extend(muscle_match)
            
            # Look for synergist muscles
            if 'Synergists:' in text or 'synergist' in text.lower():
                muscle_match = re.findall(r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)', text)
                muscles.extend(muscle_match)
            
            # Collect instructions
            if any(word in text.lower() for word in ['preparation', 'execution', 'position']):
                if len(text) > 20:  # Avoid short fragments
                    instructions.append(text)
        
        # Clean up muscles list
        exercise['muscle_groups'] = list(set([m for m in muscles if len(m) > 2]))[:5]
        
        # Join instructions
        exercise['instructions'] = ' '.join(instructions[:3]) if instructions else f"Perform {name} with proper form."
        
        # Determine equipment from name
        if any(word in name.lower() for word in ['dumbbell', 'db']):
            exercise['equipment'] = 'Dumbbell'
        elif any(word in name.lower() for word in ['barbell', 'bb']):
            exercise['equipment'] = 'Barbell'
        elif any(word in name.lower() for word in ['cable', 'machine']):
            exercise['equipment'] = 'Cable/Machine'
        elif any(word in name.lower() for word in ['bodyweight', 'pushup', 'pullup', 'squat']):
            exercise['equipment'] = 'Bodyweight'
        
        return exercise

def scrap_all(self, max_muscle_groups: int =None):
    """Scrap all exercises from ExRx"""
    print("Starting ExRx Scraper..")
    print("==" *30)

    #Get muscle group links
    muscle_groups = dict(list(muscle_groups.items())[:max_muscle_groups])

    #Scrap each muscle group
    for i , (group_name , group_url) in enumerate(muscle_groups.items(),1):
        print(f"\n{i}/len(muscle_groups)} Scraping muscle group: {group_name}")
        exercises = self.get_exercises_from_muscle_group(group_url, group_name)
        self.exercises.extend(exercises)
    print(f"\nScraping completed. Total exercises found: {len(self.exercises)}")

    return self.exercises

def save_to_json(self, filename: str):
    """Save exercises to a JSON file"""
    with open(filename, 'w' , encoding='utf-8')as f:
        json.dump(self.exercise ,f, indent=2 , ensure_ascii=False)
    print(f"Exercises saved to {filename}")

def main():
    """Main scraping function"""
    scraper = ExRxScraper()
    
    # Scrape all (or limit for testing)
    print("Choose an option:")
    print("1. Test mode (first 3 muscle groups)")
    print("2. Full scrape (all muscle groups - takes ~30-60 minutes)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        print("\n🧪 Running in TEST mode...")
        exercises = scraper.scrape_all(max_muscle_groups=3)
    else:
        print("\n🚀 Running FULL scrape...")
        print("⚠️  This will take 30-60 minutes due to respectful delays")
        confirm = input("Continue? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            exercises = scraper.scrape_all()
        else:
            print("Cancelled.")
            return
    
    # Save results
    scraper.save_to_json()
    
    # Print summary
    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE!")
    print("=" * 60)
    print(f"Total exercises: {len(exercises)}")
    
    if exercises:
        print(f"\nSample exercise:")
        print(json.dumps(exercises[0], indent=2))
        
        # Show category breakdown
        categories = {}
        for ex in exercises:
            cat = ex['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print(f"\nExercises by category:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count}")


if __name__ == "__main__":
    main()

