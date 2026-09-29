"""
Regional boundaries, City definitions, and Comprehensive Geographic Place Registry.

Provides boundary and center information for key Indian metropolitan cities,
popular urban localities, and instant local resolution.
"""

SUPPORTED_CITIES = {
    "pune": {
        "name": "Pune",
        "state": "Maharashtra",
        "center": {"latitude": 18.5204, "longitude": 73.8567},
        "bounds": {"min_lat": 18.35, "max_lat": 18.70, "min_lon": 73.65, "max_lon": 74.05},
        "zoom": 12
    },
    "delhi": {
        "name": "Delhi NCR",
        "state": "Delhi",
        "center": {"latitude": 28.6139, "longitude": 77.2090},
        "bounds": {"min_lat": 28.35, "max_lat": 28.90, "min_lon": 76.85, "max_lon": 77.45},
        "zoom": 11
    },
    "mumbai": {
        "name": "Mumbai",
        "state": "Maharashtra",
        "center": {"latitude": 19.0760, "longitude": 72.8777},
        "bounds": {"min_lat": 18.85, "max_lat": 19.35, "min_lon": 72.75, "max_lon": 73.10},
        "zoom": 11
    },
    "bengaluru": {
        "name": "Bengaluru",
        "state": "Karnataka",
        "center": {"latitude": 12.9716, "longitude": 77.5946},
        "bounds": {"min_lat": 12.80, "max_lat": 13.15, "min_lon": 77.40, "max_lon": 77.80},
        "zoom": 11
    },
    "chennai": {
        "name": "Chennai",
        "state": "Tamil Nadu",
        "center": {"latitude": 13.0827, "longitude": 80.2707},
        "bounds": {"min_lat": 12.90, "max_lat": 13.25, "min_lon": 80.10, "max_lon": 80.35},
        "zoom": 11
    },
    "kolkata": {
        "name": "Kolkata",
        "state": "West Bengal",
        "center": {"latitude": 22.5726, "longitude": 88.3639},
        "bounds": {"min_lat": 22.40, "max_lat": 22.75, "min_lon": 88.20, "max_lon": 88.50},
        "zoom": 11
    },
    "hyderabad": {
        "name": "Hyderabad",
        "state": "Telangana",
        "center": {"latitude": 17.3850, "longitude": 78.4867},
        "bounds": {"min_lat": 17.20, "max_lat": 17.60, "min_lon": 78.25, "max_lon": 78.65},
        "zoom": 11
    },
    "ahmedabad": {
        "name": "Ahmedabad",
        "state": "Gujarat",
        "center": {"latitude": 23.0225, "longitude": 72.5714},
        "bounds": {"min_lat": 22.90, "max_lat": 23.15, "min_lon": 72.45, "max_lon": 72.70},
        "zoom": 11
    },
    "jaipur": {
        "name": "Jaipur",
        "state": "Rajasthan",
        "center": {"latitude": 26.9124, "longitude": 75.7873},
        "bounds": {"min_lat": 26.75, "max_lat": 27.05, "min_lon": 75.65, "max_lon": 75.95},
        "zoom": 11
    },
    "coimbatore": {
        "name": "Coimbatore",
        "state": "Tamil Nadu",
        "center": {"latitude": 11.0168, "longitude": 76.9558},
        "bounds": {"min_lat": 10.90, "max_lat": 11.15, "min_lon": 76.85, "max_lon": 77.10},
        "zoom": 12
    },
    "madurai": {
        "name": "Madurai",
        "state": "Tamil Nadu",
        "center": {"latitude": 9.9252, "longitude": 78.1198},
        "bounds": {"min_lat": 9.80, "max_lat": 10.05, "min_lon": 78.00, "max_lon": 78.25},
        "zoom": 12
    },
    "trichy": {
        "name": "Tiruchirappalli (Trichy)",
        "state": "Tamil Nadu",
        "center": {"latitude": 10.7905, "longitude": 78.7047},
        "bounds": {"min_lat": 10.70, "max_lat": 10.90, "min_lon": 78.60, "max_lon": 78.80},
        "zoom": 12
    },
    "salem": {
        "name": "Salem",
        "state": "Tamil Nadu",
        "center": {"latitude": 11.6643, "longitude": 78.1460},
        "bounds": {"min_lat": 11.55, "max_lat": 11.75, "min_lon": 78.05, "max_lon": 78.25},
        "zoom": 12
    },
    "lucknow": {
        "name": "Lucknow",
        "state": "Uttar Pradesh",
        "center": {"latitude": 26.8467, "longitude": 80.9462},
        "bounds": {"min_lat": 26.70, "max_lat": 27.00, "min_lon": 80.80, "max_lon": 81.10},
        "zoom": 11
    },
    "chandigarh": {
        "name": "Chandigarh",
        "state": "Punjab & Haryana",
        "center": {"latitude": 30.7333, "longitude": 76.7794},
        "bounds": {"min_lat": 30.65, "max_lat": 30.82, "min_lon": 76.70, "max_lon": 76.88},
        "zoom": 12
    },
    "kochi": {
        "name": "Kochi",
        "state": "Kerala",
        "center": {"latitude": 9.9312, "longitude": 76.2673},
        "bounds": {"min_lat": 9.80, "max_lat": 10.05, "min_lon": 76.15, "max_lon": 76.40},
        "zoom": 12
    }
}

# Pune defaults
PUNE_BOUNDS = SUPPORTED_CITIES["pune"]["bounds"]
PUNE_CENTER = SUPPORTED_CITIES["pune"]["center"]

# Broad India bounds for national coverage
INDIA_BOUNDS = {
    "min_lat": 6.5,
    "max_lat": 37.5,
    "min_lon": 68.0,
    "max_lon": 97.5
}

# Comprehensive instant local place database
KNOWN_PLACES = [
    # Pune Localities
    {"name": "Kothrud", "city": "Pune", "state": "Maharashtra", "lat": 18.5074, "lon": 73.8077, "display_name": "Kothrud, Pune, Maharashtra, India"},
    {"name": "Hinjewadi Phase 1", "city": "Pune", "state": "Maharashtra", "lat": 18.5913, "lon": 73.7389, "display_name": "Hinjewadi Phase 1, Pune, Maharashtra, India"},
    {"name": "Hinjewadi Phase 2", "city": "Pune", "state": "Maharashtra", "lat": 18.5975, "lon": 73.7190, "display_name": "Hinjewadi Phase 2, Pune, Maharashtra, India"},
    {"name": "Hinjewadi Phase 3", "city": "Pune", "state": "Maharashtra", "lat": 18.5835, "lon": 73.6980, "display_name": "Hinjewadi Phase 3, Pune, Maharashtra, India"},
    {"name": "Shivajinagar", "city": "Pune", "state": "Maharashtra", "lat": 18.5314, "lon": 73.8446, "display_name": "Shivajinagar, Pune, Maharashtra, India"},
    {"name": "Viman Nagar", "city": "Pune", "state": "Maharashtra", "lat": 18.5679, "lon": 73.9143, "display_name": "Viman Nagar, Pune, Maharashtra, India"},
    {"name": "Wakad", "city": "Pune", "state": "Maharashtra", "lat": 18.5987, "lon": 73.7688, "display_name": "Wakad, Pune, Maharashtra, India"},
    {"name": "Baner", "city": "Pune", "state": "Maharashtra", "lat": 18.5590, "lon": 73.7868, "display_name": "Baner, Pune, Maharashtra, India"},
    {"name": "Hadapsar", "city": "Pune", "state": "Maharashtra", "lat": 18.5089, "lon": 73.9259, "display_name": "Hadapsar, Pune, Maharashtra, India"},
    {"name": "Aundh", "city": "Pune", "state": "Maharashtra", "lat": 18.5602, "lon": 73.8031, "display_name": "Aundh, Pune, Maharashtra, India"},
    {"name": "Magarpatta City", "city": "Pune", "state": "Maharashtra", "lat": 18.5147, "lon": 73.9298, "display_name": "Magarpatta City, Pune, Maharashtra, India"},
    {"name": "Kalyani Nagar", "city": "Pune", "state": "Maharashtra", "lat": 18.5477, "lon": 73.9022, "display_name": "Kalyani Nagar, Pune, Maharashtra, India"},
    {"name": "Koregaon Park", "city": "Pune", "state": "Maharashtra", "lat": 18.5362, "lon": 73.8940, "display_name": "Koregaon Park, Pune, Maharashtra, India"},
    {"name": "FC Road", "city": "Pune", "state": "Maharashtra", "lat": 18.5240, "lon": 73.8415, "display_name": "FC Road, Deccan Gymkhana, Pune, Maharashtra, India"},
    {"name": "JM Road", "city": "Pune", "state": "Maharashtra", "lat": 18.5220, "lon": 73.8450, "display_name": "JM Road, Shivajinagar, Pune, Maharashtra, India"},
    {"name": "Deccan Gymkhana", "city": "Pune", "state": "Maharashtra", "lat": 18.5173, "lon": 73.8417, "display_name": "Deccan Gymkhana, Pune, Maharashtra, India"},
    {"name": "Swargate", "city": "Pune", "state": "Maharashtra", "lat": 18.5018, "lon": 73.8585, "display_name": "Swargate, Pune, Maharashtra, India"},
    {"name": "Katraj", "city": "Pune", "state": "Maharashtra", "lat": 18.4575, "lon": 73.8677, "display_name": "Katraj, Pune, Maharashtra, India"},
    {"name": "Pimpri", "city": "Pune", "state": "Maharashtra", "lat": 18.6279, "lon": 73.7997, "display_name": "Pimpri, PCMC, Pune, Maharashtra, India"},
    {"name": "Chinchwad", "city": "Pune", "state": "Maharashtra", "lat": 18.6298, "lon": 73.7997, "display_name": "Chinchwad, PCMC, Pune, Maharashtra, India"},
    {"name": "Kharadi", "city": "Pune", "state": "Maharashtra", "lat": 18.5516, "lon": 73.9352, "display_name": "Kharadi, Pune, Maharashtra, India"},
    {"name": "Bavdhan", "city": "Pune", "state": "Maharashtra", "lat": 18.5126, "lon": 73.7712, "display_name": "Bavdhan, Pune, Maharashtra, India"},
    {"name": "Pashan", "city": "Pune", "state": "Maharashtra", "lat": 18.5415, "lon": 73.7925, "display_name": "Pashan, Pune, Maharashtra, India"},
    {"name": "Pune City Center", "city": "Pune", "state": "Maharashtra", "lat": 18.5204, "lon": 73.8567, "display_name": "Pune, Maharashtra, India"},

    # Tamil Nadu Cities & Localities
    {"name": "Chennai", "city": "Chennai", "state": "Tamil Nadu", "lat": 13.0827, "lon": 80.2707, "display_name": "Chennai, Tamil Nadu, India"},
    {"name": "T. Nagar", "city": "Chennai", "state": "Tamil Nadu", "lat": 13.0418, "lon": 80.2341, "display_name": "T. Nagar, Chennai, Tamil Nadu, India"},
    {"name": "Anna Nagar", "city": "Chennai", "state": "Tamil Nadu", "lat": 13.0850, "lon": 80.2101, "display_name": "Anna Nagar, Chennai, Tamil Nadu, India"},
    {"name": "Adyar", "city": "Chennai", "state": "Tamil Nadu", "lat": 13.0012, "lon": 80.2565, "display_name": "Adyar, Chennai, Tamil Nadu, India"},
    {"name": "Velachery", "city": "Chennai", "state": "Tamil Nadu", "lat": 12.9815, "lon": 80.2180, "display_name": "Velachery, Chennai, Tamil Nadu, India"},
    {"name": "Guindy", "city": "Chennai", "state": "Tamil Nadu", "lat": 13.0067, "lon": 80.2025, "display_name": "Guindy, Chennai, Tamil Nadu, India"},
    {"name": "Tambaram", "city": "Chennai", "state": "Tamil Nadu", "lat": 12.9249, "lon": 80.1000, "display_name": "Tambaram, Chennai, Tamil Nadu, India"},
    {"name": "OMR (Old Mahabalipuram Road)", "city": "Chennai", "state": "Tamil Nadu", "lat": 12.9360, "lon": 80.2310, "display_name": "OMR, Chennai, Tamil Nadu, India"},
    {"name": "Coimbatore", "city": "Coimbatore", "state": "Tamil Nadu", "lat": 11.0168, "lon": 76.9558, "display_name": "Coimbatore, Tamil Nadu, India"},
    {"name": "Gandhipuram", "city": "Coimbatore", "state": "Tamil Nadu", "lat": 11.0183, "lon": 76.9644, "display_name": "Gandhipuram, Coimbatore, Tamil Nadu, India"},
    {"name": "RS Puram", "city": "Coimbatore", "state": "Tamil Nadu", "lat": 11.0118, "lon": 76.9472, "display_name": "RS Puram, Coimbatore, Tamil Nadu, India"},
    {"name": "Peelamedu", "city": "Coimbatore", "state": "Tamil Nadu", "lat": 11.0297, "lon": 77.0041, "display_name": "Peelamedu, Coimbatore, Tamil Nadu, India"},
    {"name": "Madurai", "city": "Madurai", "state": "Tamil Nadu", "lat": 9.9252, "lon": 78.1198, "display_name": "Madurai, Tamil Nadu, India"},
    {"name": "Tiruchirappalli (Trichy)", "city": "Tiruchirappalli", "state": "Tamil Nadu", "lat": 10.7905, "lon": 78.7047, "display_name": "Tiruchirappalli (Trichy), Tamil Nadu, India"},
    {"name": "Salem", "city": "Salem", "state": "Tamil Nadu", "lat": 11.6643, "lon": 78.1460, "display_name": "Salem, Tamil Nadu, India"},
    {"name": "Tirunelveli", "city": "Tirunelveli", "state": "Tamil Nadu", "lat": 8.7139, "lon": 77.7567, "display_name": "Tirunelveli, Tamil Nadu, India"},
    {"name": "Erode", "city": "Erode", "state": "Tamil Nadu", "lat": 11.3410, "lon": 77.7172, "display_name": "Erode, Tamil Nadu, India"},
    {"name": "Vellore", "city": "Vellore", "state": "Tamil Nadu", "lat": 12.9165, "lon": 79.1325, "display_name": "Vellore, Tamil Nadu, India"},
    {"name": "Thanjavur", "city": "Thanjavur", "state": "Tamil Nadu", "lat": 10.7870, "lon": 79.1378, "display_name": "Thanjavur, Tamil Nadu, India"},
    {"name": "Tiruppur", "city": "Tiruppur", "state": "Tamil Nadu", "lat": 11.1085, "lon": 77.3411, "display_name": "Tiruppur, Tamil Nadu, India"},
    {"name": "Dindigul", "city": "Dindigul", "state": "Tamil Nadu", "lat": 10.3673, "lon": 77.9803, "display_name": "Dindigul, Tamil Nadu, India"},
    {"name": "Kanchipuram", "city": "Kanchipuram", "state": "Tamil Nadu", "lat": 12.8342, "lon": 79.7036, "display_name": "Kanchipuram, Tamil Nadu, India"},
    {"name": "Thoothukudi", "city": "Thoothukudi", "state": "Tamil Nadu", "lat": 8.7642, "lon": 78.1348, "display_name": "Thoothukudi, Tamil Nadu, India"},
    {"name": "Hosur", "city": "Hosur", "state": "Tamil Nadu", "lat": 12.7409, "lon": 77.8253, "display_name": "Hosur, Tamil Nadu, India"},
    {"name": "Ooty", "city": "The Nilgiris", "state": "Tamil Nadu", "lat": 11.4102, "lon": 76.6950, "display_name": "Ooty (Udhagamandalam), Tamil Nadu, India"},

    # Delhi NCR Localities
    {"name": "Delhi NCR", "city": "Delhi", "state": "Delhi", "lat": 28.6139, "lon": 77.2090, "display_name": "Delhi NCR, Delhi, India"},
    {"name": "New Delhi", "city": "New Delhi", "state": "Delhi", "lat": 28.6139, "lon": 77.2090, "display_name": "New Delhi, Delhi, India"},
    {"name": "Connaught Place", "city": "New Delhi", "state": "Delhi", "lat": 28.6315, "lon": 77.2167, "display_name": "Connaught Place, New Delhi, Delhi, India"},
    {"name": "Karol Bagh", "city": "New Delhi", "state": "Delhi", "lat": 28.6517, "lon": 77.1906, "display_name": "Karol Bagh, New Delhi, Delhi, India"},
    {"name": "Hauz Khas", "city": "New Delhi", "state": "Delhi", "lat": 28.5494, "lon": 77.2001, "display_name": "Hauz Khas, New Delhi, Delhi, India"},
    {"name": "Rohini", "city": "Delhi", "state": "Delhi", "lat": 28.7495, "lon": 77.0565, "display_name": "Rohini, Delhi, India"},
    {"name": "Dwarka", "city": "Delhi", "state": "Delhi", "lat": 28.5921, "lon": 77.0460, "display_name": "Dwarka, New Delhi, Delhi, India"},
    {"name": "Noida", "city": "Noida", "state": "Uttar Pradesh", "lat": 28.5355, "lon": 77.3910, "display_name": "Noida, Gautam Buddha Nagar, Uttar Pradesh, India"},
    {"name": "Gurgaon (Gurugram)", "city": "Gurugram", "state": "Haryana", "lat": 28.4595, "lon": 77.0266, "display_name": "Gurugram (Gurgaon), Haryana, India"},
    {"name": "Ghaziabad", "city": "Ghaziabad", "state": "Uttar Pradesh", "lat": 28.6692, "lon": 77.4538, "display_name": "Ghaziabad, Uttar Pradesh, India"},
    {"name": "Faridabad", "city": "Faridabad", "state": "Haryana", "lat": 28.4089, "lon": 77.3178, "display_name": "Faridabad, Haryana, India"},

    # Mumbai Localities
    {"name": "Mumbai", "city": "Mumbai", "state": "Maharashtra", "lat": 19.0760, "lon": 72.8777, "display_name": "Mumbai, Maharashtra, India"},
    {"name": "Bandra", "city": "Mumbai", "state": "Maharashtra", "lat": 19.0596, "lon": 72.8295, "display_name": "Bandra, Mumbai, Maharashtra, India"},
    {"name": "Andheri", "city": "Mumbai", "state": "Maharashtra", "lat": 19.1136, "lon": 72.8697, "display_name": "Andheri, Mumbai, Maharashtra, India"},
    {"name": "Colaba", "city": "Mumbai", "state": "Maharashtra", "lat": 18.9067, "lon": 72.8147, "display_name": "Colaba, South Mumbai, Maharashtra, India"},
    {"name": "Dadar", "city": "Mumbai", "state": "Maharashtra", "lat": 19.0178, "lon": 72.8478, "display_name": "Dadar, Mumbai, Maharashtra, India"},
    {"name": "Borivali", "city": "Mumbai", "state": "Maharashtra", "lat": 19.2307, "lon": 72.8567, "display_name": "Borivali, Mumbai, Maharashtra, India"},
    {"name": "Navi Mumbai", "city": "Navi Mumbai", "state": "Maharashtra", "lat": 19.0330, "lon": 73.0297, "display_name": "Navi Mumbai, Maharashtra, India"},
    {"name": "Thane", "city": "Thane", "state": "Maharashtra", "lat": 19.2183, "lon": 72.9781, "display_name": "Thane, Maharashtra, India"},

    # Bengaluru Localities
    {"name": "Bengaluru", "city": "Bengaluru", "state": "Karnataka", "lat": 12.9716, "lon": 77.5946, "display_name": "Bengaluru, Karnataka, India"},
    {"name": "Koramangala", "city": "Bengaluru", "state": "Karnataka", "lat": 12.9352, "lon": 77.6245, "display_name": "Koramangala, Bengaluru, Karnataka, India"},
    {"name": "Indiranagar", "city": "Bengaluru", "state": "Karnataka", "lat": 12.9784, "lon": 77.6408, "display_name": "Indiranagar, Bengaluru, Karnataka, India"},
    {"name": "Whitefield", "city": "Bengaluru", "state": "Karnataka", "lat": 12.9698, "lon": 77.7499, "display_name": "Whitefield, Bengaluru, Karnataka, India"},
    {"name": "Electronic City", "city": "Bengaluru", "state": "Karnataka", "lat": 12.8452, "lon": 77.6602, "display_name": "Electronic City, Bengaluru, Karnataka, India"},
    {"name": "HSR Layout", "city": "Bengaluru", "state": "Karnataka", "lat": 12.9121, "lon": 77.6446, "display_name": "HSR Layout, Bengaluru, Karnataka, India"},

    # Hyderabad Localities
    {"name": "Hyderabad", "city": "Hyderabad", "state": "Telangana", "lat": 17.3850, "lon": 78.4867, "display_name": "Hyderabad, Telangana, India"},
    {"name": "Hitec City", "city": "Hyderabad", "state": "Telangana", "lat": 17.4435, "lon": 78.3772, "display_name": "Hitec City, Hyderabad, Telangana, India"},
    {"name": "Gachibowli", "city": "Hyderabad", "state": "Telangana", "lat": 17.4401, "lon": 78.3489, "display_name": "Gachibowli, Hyderabad, Telangana, India"},
    {"name": "Banjara Hills", "city": "Hyderabad", "state": "Telangana", "lat": 17.4156, "lon": 78.4350, "display_name": "Banjara Hills, Hyderabad, Telangana, India"},
    {"name": "Secunderabad", "city": "Hyderabad", "state": "Telangana", "lat": 17.4399, "lon": 78.4983, "display_name": "Secunderabad, Telangana, India"},

    # Kolkata Localities
    {"name": "Kolkata", "city": "Kolkata", "state": "West Bengal", "lat": 22.5726, "lon": 88.3639, "display_name": "Kolkata, West Bengal, India"},
    {"name": "Salt Lake", "city": "Kolkata", "state": "West Bengal", "lat": 22.5867, "lon": 88.4178, "display_name": "Salt Lake (Bidhannagar), Kolkata, West Bengal, India"},
    {"name": "Howrah", "city": "Howrah", "state": "West Bengal", "lat": 22.5958, "lon": 88.2636, "display_name": "Howrah, West Bengal, India"},
    {"name": "Park Street", "city": "Kolkata", "state": "West Bengal", "lat": 22.5516, "lon": 88.3524, "display_name": "Park Street, Kolkata, West Bengal, India"},

    # Other Major Indian Metros
    {"name": "Ahmedabad", "city": "Ahmedabad", "state": "Gujarat", "lat": 23.0225, "lon": 72.5714, "display_name": "Ahmedabad, Gujarat, India"},
    {"name": "Jaipur", "city": "Jaipur", "state": "Rajasthan", "lat": 26.9124, "lon": 75.7873, "display_name": "Jaipur, Rajasthan, India"},
    {"name": "Lucknow", "city": "Lucknow", "state": "Uttar Pradesh", "lat": 26.8467, "lon": 80.9462, "display_name": "Lucknow, Uttar Pradesh, India"},
    {"name": "Chandigarh", "city": "Chandigarh", "state": "Punjab & Haryana", "lat": 30.7333, "lon": 76.7794, "display_name": "Chandigarh, India"},
    {"name": "Kochi (Cochin)", "city": "Kochi", "state": "Kerala", "lat": 9.9312, "lon": 76.2673, "display_name": "Kochi, Kerala, India"},
    {"name": "Indore", "city": "Indore", "state": "Madhya Pradesh", "lat": 22.7196, "lon": 75.8577, "display_name": "Indore, Madhya Pradesh, India"},
    {"name": "Bhopal", "city": "Bhopal", "state": "Madhya Pradesh", "lat": 23.2599, "lon": 77.4126, "display_name": "Bhopal, Madhya Pradesh, India"},
    {"name": "Surat", "city": "Surat", "state": "Gujarat", "lat": 21.1702, "lon": 72.8311, "display_name": "Surat, Gujarat, India"},
    {"name": "Patna", "city": "Patna", "state": "Bihar", "lat": 25.5941, "lon": 85.1376, "display_name": "Patna, Bihar, India"},
    {"name": "Visakhapatnam (Vizag)", "city": "Visakhapatnam", "state": "Andhra Pradesh", "lat": 17.6868, "lon": 83.2185, "display_name": "Visakhapatnam, Andhra Pradesh, India"},
    {"name": "Vijayawada", "city": "Vijayawada", "state": "Andhra Pradesh", "lat": 16.5062, "lon": 80.6480, "display_name": "Vijayawada, Andhra Pradesh, India"},
    {"name": "Nagpur", "city": "Nagpur", "state": "Maharashtra", "lat": 21.1458, "lon": 79.0882, "display_name": "Nagpur, Maharashtra, India"},
    {"name": "Nashik", "city": "Nashik", "state": "Maharashtra", "lat": 19.9975, "lon": 73.7898, "display_name": "Nashik, Maharashtra, India"},
    {"name": "Varanasi", "city": "Varanasi", "state": "Uttar Pradesh", "lat": 25.3176, "lon": 82.9739, "display_name": "Varanasi, Uttar Pradesh, India"},
    {"name": "Agra", "city": "Agra", "state": "Uttar Pradesh", "lat": 27.1767, "lon": 78.0081, "display_name": "Agra, Uttar Pradesh, India"},
    {"name": "Amritsar", "city": "Amritsar", "state": "Punjab", "lat": 31.6340, "lon": 74.8723, "display_name": "Amritsar, Punjab, India"},
    {"name": "Bhubaneswar", "city": "Bhubaneswar", "state": "Odisha", "lat": 20.2961, "lon": 85.8245, "display_name": "Bhubaneswar, Odisha, India"},
    {"name": "Thiruvananthapuram", "city": "Thiruvananthapuram", "state": "Kerala", "lat": 8.5241, "lon": 76.9366, "display_name": "Thiruvananthapuram, Kerala, India"},
    {"name": "Goa (Panaji)", "city": "Panaji", "state": "Goa", "lat": 15.4909, "lon": 73.8278, "display_name": "Panaji, Goa, India"},
    {"name": "Guwahati", "city": "Guwahati", "state": "Assam", "lat": 26.1445, "lon": 91.7362, "display_name": "Guwahati, Assam, India"}
]


def is_within_pune(latitude: float, longitude: float) -> bool:
    """Checks if coordinates fall within Pune bounding area."""
    return (
        PUNE_BOUNDS["min_lat"] <= latitude <= PUNE_BOUNDS["max_lat"]
        and PUNE_BOUNDS["min_lon"] <= longitude <= PUNE_BOUNDS["max_lon"]
    )


def is_valid_location(latitude: float, longitude: float) -> bool:
    """Validates that latitude and longitude are valid global coordinates."""
    return (-90.0 <= latitude <= 90.0) and (-180.0 <= longitude <= 180.0)


def detect_city(latitude: float, longitude: float) -> str:
    """Detects which supported city the coordinate belongs to, or defaults to closest/pune."""
    for city_key, data in SUPPORTED_CITIES.items():
        b = data["bounds"]
        if b["min_lat"] <= latitude <= b["max_lat"] and b["min_lon"] <= longitude <= b["max_lon"]:
            return city_key
    return "pune"
