# MyCommute

MyCommute is an intelligent journey planning application that provides optimized route recommendations based on user preferences and sustainability goals. The application uses symbolic regression and machine learning techniques to personalize route suggestions while considering factors such as safety, air quality, and scenic value.

## Features

- **Interactive Map Interface**: Powered by Mapbox GL JS for seamless route visualization
- **Multiple Travel Modes**: Support for walking, cycling, driving, and traffic-optimized driving
- **Personalized Route Optimization**: Set custom weights for various factors:
  - Safety score
  - Air quality
  - Scenic value
  - Travel time
  - Distance
- **User Authentication**: Secure account creation and management
- **Smart Route Recommendations**: Uses symbolic regression to learn from user preferences and provide optimized routes
- **Real-time Data Integration**: Leverages Mapbox Direction API for current route information

## Technology Stack

### Frontend
- HTML/CSS/JavaScript
- Mapbox GL JS

### Backend
- Python
- Flask
- SQLAlchemy
- gplearn (Symbolic Regression)
- NumPy, Pandas

### External Services
- Mapbox Direction API

## Installation

1. Clone the repository
```bash
git clone [repository-url]
cd mycommute
```

2. Install required dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
export MAPBOX_ACCESS_TOKEN='your_mapbox_token'
export FLASK_APP=app.py
export FLASK_ENV=development
```

4. Initialize the database
```bash
flask db upgrade
```

5. Run the application
```bash
flask run
```

## Usage

1. Create an account or log in to your existing account
2. Set your route preferences using the "Set Weights" button
3. Choose your travel mode (walking, cycling, driving, or traffic)
4. Select your start point and destination on the map
5. Review the optimized routes provided based on your preferences
6. Select your preferred route to begin navigation

## Testing

The application includes automated tests using Selenium and unittest. To run the tests:

```bash
python -m unittest discover tests
```

## Architecture

The application follows a modular architecture:
- Frontend: User interface and map rendering
- Backend Services: Authentication and route optimization
- Databases: User information and route data storage
- External Services: Integration with Mapbox API

## Future Enhancements

- Integration of real-world sustainability data
- Multi-objective optimization using NSGA-II/III which is demoed in jupyter notebook file(Pymoo_multi_objective_optimization_experiment.ipynb)
- Enhanced visualization of preference impacts
- Mobile application development
- Integration with additional mapping services

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

Copyright (c) 2024 daniel okeoghene akalamudo 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contact

mobile:- +447831590475

email:- danielakalamudo@gmail.com

## Acknowledgments

- Mapbox for providing the mapping services
- Flask and Python communities for the robust backend framework
- Contributors and testers who helped improve the application
