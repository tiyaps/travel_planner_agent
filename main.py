# FILE: main.py
# WHERE TO PLACE: In the root folder (travel-planner-agent/)
# THIS IS THE FILE YOU WILL RUN!

import sys
sys.path.append('.')

from agents.travel_planner_agent import TravelPlannerAgent

def get_user_input():
    """
    This function asks the user for their preferences
    """
    print("\n" + "🌍 "*20)
    print("      WELCOME TO AI TRAVEL PLANNER AGENT      ")
    print("🌍 "*20)
    
    # Get budget
    print("\n💰 BUDGET:")
    print("   Enter your total budget in INR (e.g., 50000)")
    while True:
        try:
            budget = int(input("   Budget: ₹"))
            if budget > 0:
                break
            print("   ❌ Budget must be positive!")
        except ValueError:
            print("   ❌ Enter a valid number!")
    
    # Get number of days
    print("\n📅 TRIP DURATION:")
    print("   How many days? (e.g., 5)")
    while True:
        try:
            num_days = int(input("   Days: "))
            if 1 <= num_days <= 30:
                break
            print("   ❌ Enter days between 1 and 30!")
        except ValueError:
            print("   ❌ Enter a valid number!")
    
    # Get city
    print("\n🏙️  DESTINATION:")
    print("   Available cities: Delhi, Mumbai, Bangalore, Goa")
    while True:
        city = input("   City: ").title()
        valid_cities = ['Delhi', 'Mumbai', 'Bangalore', 'Goa']
        if city in valid_cities:
            break
        print(f"   ❌ Enter one of: {', '.join(valid_cities)}")
    
    # Get activity preferences
    print("\n🎯 ACTIVITY PREFERENCES:")
    print("   Available: historical, sightseeing, adventure, relaxation")
    print("            shopping, entertainment, nature, educational")
    print("   Enter preferences (comma-separated, e.g., adventure,nature)")
    print("   Or type 'all' for all types")
    preferences_input = input("   Preferences: ").lower().strip()
    
    if preferences_input.lower() == 'all':
        activity_preferences = ['all']
    else:
        activity_preferences = [p.strip() for p in preferences_input.split(',')]
    
    return budget, num_days, city, activity_preferences


def main():
    """
    Main function - this is where everything starts
    """
    # Get user input
    budget, num_days, city, activity_preferences = get_user_input()
    
    # Create the agent
    agent = TravelPlannerAgent(
        budget=budget,
        num_days=num_days,
        city=city,
        activity_preferences=activity_preferences
    )
    
    # Run the agent (this is where the magic happens!)
    result = agent.run()
    
    # Ask if user wants to save or modify
    print("\n" + "="*60)
    print("SAVE OR MODIFY?")
    print("="*60)
    print("\n1. Save itinerary to file")
    print("2. Create another plan")
    print("3. Exit")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == '1':
        filename = f"itinerary_{city}_{num_days}days.txt"
        save_itinerary(filename, result, budget, num_days, city)
    elif choice == '2':
        main()  # Restart
    else:
        print("\n👋 Thank you for using Travel Planner Agent!")


def save_itinerary(filename, result, budget, num_days, city):
    """
    Save the itinerary to a text file
    """
    with open(filename, 'w') as f:
        f.write("="*60 + "\n")
        f.write("TRAVEL ITINERARY\n")
        f.write("="*60 + "\n\n")
        
        f.write(f"DESTINATION: {city}\n")
        f.write(f"DURATION: {num_days} days\n")
        f.write(f"BUDGET: ₹{budget:,.0f}\n\n")
        
        f.write("DAY-BY-DAY PLAN:\n")
        f.write("-"*60 + "\n")
        
        daily_plan = result['daily_plan']
        for day in range(1, num_days + 1):
            plan = daily_plan.get(day, {})
            f.write(f"\nDAY {day}:\n")
            
            if plan.get('activities'):
                for activity in plan['activities']:
                    f.write(f"  • {activity['name']} ({activity['duration']}h) - ₹{activity['cost']}\n")
            else:
                f.write(f"  • Rest day / Free exploration\n")
            
            f.write(f"  Activity Cost: ₹{plan.get('total_cost', 0)}\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("COST BREAKDOWN:\n")
        f.write("="*60 + "\n")
        
        cost_breakdown = result['cost_breakdown']
        for category, cost in cost_breakdown.items():
            f.write(f"{category.capitalize():.<30} ₹{cost:>10,.0f}\n")
        
        f.write("\n" + "-"*60 + "\n")
        remaining = budget - cost_breakdown['total']
        f.write(f"REMAINING: ₹{remaining:,.0f}\n")
    
    print(f"\n✅ Itinerary saved to '{filename}'")


if __name__ == "__main__":
    main()