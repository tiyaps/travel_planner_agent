# FILE: agents/travel_planner_agent.py
# WHERE TO PLACE: Inside the agents folder
# This is the BRAIN of the travel planner - where the logic lives

import sys
sys.path.append('..')
from config.travel_config import (
    BUDGET_ALLOCATION, ACTIVITIES_DATABASE, HOTEL_PRICES, 
    DAILY_MEAL_COST, MAX_HOURS_PER_DAY, BUFFER_PERCENTAGE
)

class TravelPlannerAgent:
    """
    This is the main agent that plans your travel.
    Think of it like a travel agent that thinks step by step.
    """
    
    def __init__(self, budget, num_days, city, activity_preferences):
        """
        Initialize the agent with user inputs
        
        Args:
            budget: Total budget in INR
            num_days: Number of days for trip
            city: Which city to visit
            activity_preferences: List of preferred activities (e.g., ['adventure', 'historical'])
        """
        self.budget = budget
        self.num_days = num_days
        self.city = city
        self.activity_preferences = activity_preferences
        self.plan = {}
        self.spent = 0
        self.iterations = 0
        
    def step_1_allocate_budget(self):
        """
        STEP 1: Break down the budget into categories
        Think of dividing a pizza into slices
        """
        print("\n" + "="*60)
        print("STEP 1: ALLOCATING BUDGET")
        print("="*60)
        
        allocation = {}
        for category, percentage in BUDGET_ALLOCATION.items():
            amount = self.budget * percentage
            allocation[category] = amount
            print(f"  {category.upper()}: ₹{amount:,.0f} ({percentage*100:.0f}%)")
        
        self.allocated_budget = allocation
        print(f"\nTotal Budget: ₹{self.budget:,.0f}")
        return allocation
    
    def step_2_select_activities(self):
        """
        STEP 2: Select activities based on preferences and budget
        Like choosing which attractions to visit
        """
        print("\n" + "="*60)
        print("STEP 2: SELECTING ACTIVITIES")
        print("="*60)
        
        if self.city not in ACTIVITIES_DATABASE:
            print(f"❌ City '{self.city}' not in database. Available: {list(ACTIVITIES_DATABASE.keys())}")
            return []
        
        all_activities = ACTIVITIES_DATABASE[self.city]
        
        # Filter activities by preference
        filtered = {}
        for activity_name, activity_info in all_activities.items():
            # Check if activity matches preference
            if activity_info['category'] in self.activity_preferences or 'all' in self.activity_preferences:
                filtered[activity_name] = activity_info
        
        if not filtered:
            # If no matches, use all activities
            filtered = all_activities
            print(f"⚠️  No activities match preferences. Showing all available.")
        
        print(f"\n📍 Activities available in {self.city}:")
        for name, info in filtered.items():
            print(f"  • {name} - ₹{info['cost']} ({info['duration']}h) [{info['category']}]")
        
        self.selected_activities = filtered
        return filtered
    
    def step_3_create_daily_plan(self):
        """
        STEP 3: Break the itinerary into days
        Like scheduling which day to do what
        """
        print("\n" + "="*60)
        print("STEP 3: CREATING DAILY PLAN")
        print("="*60)
        
        self.daily_plan = {}
        activities_list = list(self.selected_activities.items())
        activities_per_day = max(1, len(activities_list) // self.num_days)
        
        activity_idx = 0
        for day in range(1, self.num_days + 1):
            self.daily_plan[day] = {
                'activities': [],
                'total_hours': 0,
                'total_cost': 0
            }
            
            # Add activities for this day
            activities_today = 0
            while activities_today < activities_per_day and activity_idx < len(activities_list):
                activity_name, activity_info = activities_list[activity_idx]
                
                # Check if adding this would exceed time limit
                if (self.daily_plan[day]['total_hours'] + activity_info['duration'] <= MAX_HOURS_PER_DAY):
                    self.daily_plan[day]['activities'].append({
                        'name': activity_name,
                        'cost': activity_info['cost'],
                        'duration': activity_info['duration'],
                        'category': activity_info['category']
                    })
                    self.daily_plan[day]['total_hours'] += activity_info['duration']
                    self.daily_plan[day]['total_cost'] += activity_info['cost']
                    activities_today += 1
                    activity_idx += 1
                else:
                    activity_idx += 1
        
        # Print daily plan
        for day, plan in self.daily_plan.items():
            print(f"\n📅 DAY {day}:")
            if plan['activities']:
                for activity in plan['activities']:
                    print(f"   • {activity['name']} (₹{activity['cost']}, {activity['duration']}h)")
            print(f"   Total: ₹{plan['total_cost']} | {plan['total_hours']}h")
        
        return self.daily_plan
    
    def step_4_calculate_total_cost(self):
        """
        STEP 4: Calculate if we're within budget
        Like checking your bank account
        """
        print("\n" + "="*60)
        print("STEP 4: CALCULATING TOTAL COST")
        print("="*60)
        
        # Get hotel price
        hotel_price = HOTEL_PRICES[self.city]['mid']  # Using mid-range
        accommodation_cost = hotel_price * self.num_days
        
        # Get meal costs
        meal_price = DAILY_MEAL_COST[self.city]
        food_cost = meal_price * self.num_days
        
        # Get activity costs
        activity_cost = sum(plan['total_cost'] for plan in self.daily_plan.values())
        
        # Transport cost (fixed estimate)
        transport_cost = 500 * self.num_days
        
        # Total
        total_cost = accommodation_cost + food_cost + activity_cost + transport_cost
        buffer_cost = total_cost * BUFFER_PERCENTAGE
        final_cost = total_cost + buffer_cost
        
        print(f"\n💰 COST BREAKDOWN:")
        print(f"  Accommodation ({self.num_days} nights): ₹{accommodation_cost:,.0f}")
        print(f"  Food ({self.num_days} days):           ₹{food_cost:,.0f}")
        print(f"  Activities:                          ₹{activity_cost:,.0f}")
        print(f"  Transport:                           ₹{transport_cost:,.0f}")
        print(f"  Buffer (10%):                        ₹{buffer_cost:,.0f}")
        print(f"  {'─'*40}")
        print(f"  TOTAL ESTIMATED COST:                ₹{final_cost:,.0f}")
        
        print(f"\n🏦 YOUR BUDGET:                         ₹{self.budget:,.0f}")
        
        difference = self.budget - final_cost
        if difference >= 0:
            print(f"✅ WITHIN BUDGET! Remaining: ₹{difference:,.0f}")
            self.is_within_budget = True
        else:
            print(f"❌ EXCEEDS BUDGET by: ₹{abs(difference):,.0f}")
            self.is_within_budget = False
        
        self.cost_breakdown = {
            'accommodation': accommodation_cost,
            'food': food_cost,
            'activities': activity_cost,
            'transport': transport_cost,
            'buffer': buffer_cost,
            'total': final_cost
        }
        
        return self.cost_breakdown
    
    def step_5_replan_if_needed(self):
        """
        STEP 5: If over budget, remove expensive activities and retry
        Like cutting corners when things are too expensive
        """
        print("\n" + "="*60)
        print("STEP 5: REPLANNING IF NEEDED")
        print("="*60)
        
        if self.is_within_budget:
            print("✅ Plan is within budget. No replanning needed!")
            return True
        
        self.iterations += 1
        if self.iterations > 3:
            print("⚠️  Tried replanning 3 times. Showing best attempt.")
            return False
        
        print(f"🔄 REPLAN ATTEMPT #{self.iterations}")
        print("Removing most expensive activities...")
        
        # Remove activities in order of cost (expensive first)
        for day in self.daily_plan.values():
            if day['activities']:
                # Sort by cost (descending) and remove the most expensive
                day['activities'].sort(key=lambda x: x['cost'], reverse=True)
                removed = day['activities'].pop(0)
                day['total_cost'] -= removed['cost']
                day['total_hours'] -= removed['duration']
                print(f"  Removed: {removed['name']} (was ₹{removed['cost']})")
        
        # Recalculate and check
        self.step_4_calculate_total_cost()
        
        if not self.is_within_budget:
            # Try again
            return self.step_5_replan_if_needed()
        
        return True
    
    def generate_final_itinerary(self):
        """
        FINAL STEP: Generate the complete travel plan
        """
        print("\n" + "="*60)
        print("🎉 FINAL TRAVEL ITINERARY")
        print("="*60)
        
        print(f"\n📍 TRIP DETAILS:")
        print(f"  Destination: {self.city}")
        print(f"  Duration: {self.num_days} days")
        print(f"  Budget: ₹{self.budget:,.0f}")
        
        print(f"\n📅 DAY-BY-DAY BREAKDOWN:")
        for day in range(1, self.num_days + 1):
            plan = self.daily_plan.get(day, {})
            print(f"\n  DAY {day}:")
            print(f"  ├─ Check-in at hotel")
            
            if plan.get('activities'):
                for i, activity in enumerate(plan['activities'], 1):
                    print(f"  ├─ {i}. {activity['name']} ({activity['duration']}h) - ₹{activity['cost']}")
            else:
                print(f"  ├─ Rest day / Free exploration")
            
            print(f"  ├─ Meals throughout the day")
            print(f"  └─ Activities Cost: ₹{plan.get('total_cost', 0)}")
        
        print(f"\n💰 FINAL COST BREAKDOWN:")
        for category, cost in self.cost_breakdown.items():
            print(f"  {category.capitalize():.<30} ₹{cost:>10,.0f}")
        
        print(f"\n{'─'*50}")
        print(f"  {'TOTAL':.<30} ₹{self.cost_breakdown['total']:>10,.0f}")
        print(f"  {'BUDGET':.<30} ₹{self.budget:>10,.0f}")
        
        remaining = self.budget - self.cost_breakdown['total']
        print(f"  {'REMAINING':.<30} ₹{remaining:>10,.0f}")
        print(f"{'─'*50}")
        
        return {
            'daily_plan': self.daily_plan,
            'cost_breakdown': self.cost_breakdown,
            'is_within_budget': self.is_within_budget
        }
    
    def run(self):
        """
        This is the MAIN LOOP - runs all steps in order
        Like executing a recipe step by step
        """
        print("\n🚀 STARTING TRAVEL PLANNER AGENT...")
        print(f"   City: {self.city} | Days: {self.num_days} | Budget: ₹{self.budget:,.0f}")
        
        # Step 1: Allocate budget
        self.step_1_allocate_budget()
        
        # Step 2: Select activities
        self.step_2_select_activities()
        
        # Step 3: Create daily plan
        self.step_3_create_daily_plan()
        
        # Step 4: Calculate costs
        self.step_4_calculate_total_cost()
        
        # Step 5: Replan if needed (AGENTIC LOOP!)
        self.step_5_replan_if_needed()
        
        # Final: Generate itinerary
        return self.generate_final_itinerary()