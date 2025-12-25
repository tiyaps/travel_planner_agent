# FILE: config/travel_config.py
# WHERE TO PLACE: Inside the config folder
# This file stores all the configuration and rules for your travel planner

# Budget allocation percentages
BUDGET_ALLOCATION = {
    'accommodation': 0.40,    # 40% of budget for hotels/stays
    'food': 0.25,             # 25% for meals
    'activities': 0.25,       # 25% for attractions
    'transport': 0.10         # 10% for local transport
}

# Activity database with costs
ACTIVITIES_DATABASE = {
    'Delhi': {
        'Red Fort': {'cost': 500, 'duration': 3, 'category': 'historical'},
        'Taj Mahal Tour': {'cost': 1500, 'duration': 5, 'category': 'historical'},
        'India Gate': {'cost': 0, 'duration': 2, 'category': 'sightseeing'},
        'Shopping at CP': {'cost': 2000, 'duration': 4, 'category': 'shopping'},
        'Adventure Sports': {'cost': 3000, 'duration': 6, 'category': 'adventure'},
    },
    'Mumbai': {
        'Gateway of India': {'cost': 0, 'duration': 2, 'category': 'sightseeing'},
        'Marine Drive Walk': {'cost': 200, 'duration': 3, 'category': 'sightseeing'},
        'Bandra Beach Sunset': {'cost': 500, 'duration': 4, 'category': 'relaxation'},
        'Bollywood Studio Tour': {'cost': 2500, 'duration': 5, 'category': 'entertainment'},
        'Island Hopping': {'cost': 3500, 'duration': 6, 'category': 'adventure'},
    },
    'Bangalore': {
        'Vidhana Soudha': {'cost': 0, 'duration': 2, 'category': 'historical'},
        'Cubbon Park': {'cost': 100, 'duration': 3, 'category': 'nature'},
        'Lalbagh Botanical Garden': {'cost': 500, 'duration': 4, 'category': 'nature'},
        'Tech Park Tour': {'cost': 1000, 'duration': 3, 'category': 'educational'},
        'Adventure Park': {'cost': 2500, 'duration': 6, 'category': 'adventure'},
    },
    'Goa': {
        'Beach Day': {'cost': 500, 'duration': 8, 'category': 'relaxation'},
        'Water Sports': {'cost': 3000, 'duration': 6, 'category': 'adventure'},
        'Old Goa Churches': {'cost': 500, 'duration': 5, 'category': 'historical'},
        'Spice Plantation Tour': {'cost': 1500, 'duration': 4, 'category': 'nature'},
        'Nightlife Exploring': {'cost': 2000, 'duration': 5, 'category': 'entertainment'},
    }
}

# Hotel prices per night
HOTEL_PRICES = {
    'Delhi': {
        'budget': 1000,      # Budget hotels/hostels
        'mid': 3000,         # Mid-range
        'luxury': 8000       # Premium
    },
    'Mumbai': {
        'budget': 1500,
        'mid': 4000,
        'luxury': 10000
    },
    'Bangalore': {
        'budget': 1000,
        'mid': 3500,
        'luxury': 9000
    },
    'Goa': {
        'budget': 800,
        'mid': 2500,
        'luxury': 7000
    }
}

# Daily food costs
DAILY_MEAL_COST = {
    'Delhi': 400,      # INR per day
    'Mumbai': 600,
    'Bangalore': 500,
    'Goa': 400
}

# Constraints
MAX_HOURS_PER_DAY = 8          # Maximum activity hours per day
MIN_REST_HOURS = 4             # Minimum rest hours
BUFFER_PERCENTAGE = 0.10       # 10% buffer for unexpected costs