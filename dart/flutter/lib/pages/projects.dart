import 'package:flutter/material.dart';

class ProjectsPage extends StatelessWidget {
  final List<Project> projects = [
    Project(
      'E-Commerce App',
      'A full-featured e-commerce mobile application built with Flutter and Firebase.',
      ['Flutter', 'Firebase', 'Stripe API'],
      Colors.blue,
      Icons.shopping_cart,
    ),
    Project(
      'Weather App',
      'A beautiful weather application with location-based forecasts and animations.',
      ['Flutter', 'Weather API', 'Animations'],
      Colors.orange,
      Icons.wb_sunny,
    ),
    Project(
      'Task Manager',
      'A productivity app for managing daily tasks and projects with team collaboration.',
      ['Flutter', 'SQLite', 'Push Notifications'],
      Colors.green,
      Icons.task_alt,
    ),
    Project(
      'Social Media Dashboard',
      'Analytics dashboard for social media management with real-time data visualization.',
      ['Flutter', 'Charts', 'REST API'],
      Colors.purple,
      Icons.dashboard,
    ),
    Project(
      'Food Delivery App',
      'On-demand food delivery application with real-time tracking and payment integration.',
      ['Flutter', 'Google Maps', 'Payment Gateway'],
      Colors.red,
      Icons.delivery_dining,
    ),
    Project(
      'Portfolio Website',
      'Responsive portfolio website built with Flutter Web showcasing my work and skills.',
      ['Flutter Web', 'Responsive Design', 'Animations'],
      Colors.teal,
      Icons.web,
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(height: 20),
          Text(
            'My Projects',
            style: TextStyle(
              fontSize: 28,
              fontWeight: FontWeight.bold,
              color: Colors.blueGrey[800],
            ),
          ),
          SizedBox(height: 10),
          Text(
            'Here are some of the projects I\'ve worked on:',
            style: TextStyle(
              fontSize: 16,
              color: Colors.blueGrey[600],
            ),
          ),
          SizedBox(height: 30),
          GridView.builder(
            shrinkWrap: true,
            physics: NeverScrollableScrollPhysics(),
            gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: MediaQuery.of(context).size.width > 800 ? 2 : 1,
              childAspectRatio: MediaQuery.of(context).size.width > 800 ? 1.2 : 0.8,
              crossAxisSpacing: 20,
              mainAxisSpacing: 20,
            ),
            itemCount: projects.length,
            itemBuilder: (context, index) {
              return _buildProjectCard(projects[index]);
            },
          ),
          SizedBox(height: 40),
          Container(
            width: double.infinity,
            padding: EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(15),
              boxShadow: [
                BoxShadow(
                  color: Colors.black12,
                  blurRadius: 10,
                  offset: Offset(0, 5),
                ),
              ],
            ),
            child: Column(
              children: [
                Icon(
                  Icons.code,
                  size: 50,
                  color: Colors.blueGrey[400],
                ),
                SizedBox(height: 15),
                Text(
                  'Want to see more projects?',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.blueGrey[800],
                  ),
                ),
                SizedBox(height: 10),
                Text(
                  'Check out my GitHub profile for more code examples and open-source contributions.',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.blueGrey[600],
                  ),
                ),
                SizedBox(height: 15),
                ElevatedButton.icon(
                  onPressed: () {
                    // Add GitHub link functionality here
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('Opening GitHub profile...')),
                    );
                  },
                  icon: Icon(Icons.launch),
                  label: Text('Visit GitHub'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blueGrey[800],
                    foregroundColor: Colors.white,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildProjectCard(Project project) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(15),
        boxShadow: [
          BoxShadow(
            color: Colors.black12,
            blurRadius: 10,
            offset: Offset(0, 5),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            height: 80,
            decoration: BoxDecoration(
              color: project.color,
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(15),
                topRight: Radius.circular(15),
              ),
            ),
            child: Center(
              child: Icon(
                project.icon,
                size: 40,
                color: Colors.white,
              ),
            ),
          ),
          Expanded(
            child: Padding(
              padding: EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    project.title,
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Colors.blueGrey[800],
                    ),
                  ),
                  SizedBox(height: 10),
                  Expanded(
                    child: Text(
                      project.description,
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.blueGrey[600],
                        height: 1.4,
                      ),
                    ),
                  ),
                  SizedBox(height: 15),
                  Wrap(
                    spacing: 6,
                    runSpacing: 6,
                    children: project.technologies.map((tech) {
                      return Container(
                        padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: project.color.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: project.color.withOpacity(0.3)),
                        ),
                        child: Text(
                          tech,
                          style: TextStyle(
                            fontSize: 10,
                            color: project.color,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      );
                    }).toList(),
                  ),
                  SizedBox(height: 15),
                  Builder(
                    builder: (context) => ElevatedButton(
                      onPressed: () {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text('Opening ${project.title}...')),
                        );
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: project.color,
                        foregroundColor: Colors.white,
                        minimumSize: Size(double.infinity, 36),
                      ),
                      child: Text('View Project'),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class Project {
  final String title;
  final String description;
  final List<String> technologies;
  final Color color;
  final IconData icon;

  Project(this.title, this.description, this.technologies, this.color, this.icon);
}
