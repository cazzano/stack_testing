import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: EdgeInsets.all(20),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SizedBox(height: 40),
            CircleAvatar(
              radius: 80,
              backgroundColor: Colors.blueGrey[300],
              child: Icon(
                Icons.person,
                size: 80,
                color: Colors.white,
              ),
            ),
            SizedBox(height: 30),
            Text(
              'Welcome to My Portfolio',
              style: TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: Colors.blueGrey[800],
              ),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 10),
            Text(
              'John Doe',
              style: TextStyle(
                fontSize: 24,
                color: Colors.blueGrey[600],
                fontWeight: FontWeight.w500,
              ),
            ),
            SizedBox(height: 20),
            Container(
              padding: EdgeInsets.all(20),
              margin: EdgeInsets.symmetric(horizontal: 20),
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
              child: Text(
                'I am a passionate Flutter Developer with expertise in creating beautiful and functional mobile applications. I love turning ideas into reality through code.',
                style: TextStyle(
                  fontSize: 16,
                  height: 1.6,
                  color: Colors.blueGrey[700],
                ),
                textAlign: TextAlign.center,
              ),
            ),
            SizedBox(height: 40),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _buildQuickNavCard(
                  context,
                  'View Skills',
                  Icons.build,
                  Colors.green,
                  '/skills',
                ),
                SizedBox(width: 20),
                _buildQuickNavCard(
                  context,
                  'My Projects',
                  Icons.work,
                  Colors.orange,
                  '/projects',
                ),
              ],
            ),
            SizedBox(height: 20),
            _buildQuickNavCard(
              context,
              'Get in Touch',
              Icons.contact_mail,
              Colors.blue,
              '/contact',
            ),
            SizedBox(height: 40),
          ],
        ),
      ),
    );
  }

  Widget _buildQuickNavCard(BuildContext context, String title, IconData icon, Color color, String route) {
    return InkWell(
      onTap: () {
        Navigator.pushReplacementNamed(context, route);
      },
      child: Container(
        padding: EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(15),
          boxShadow: [
            BoxShadow(
              color: Colors.black12,
              blurRadius: 8,
              offset: Offset(0, 4),
            ),
          ],
        ),
        child: Column(
          children: [
            Icon(
              icon,
              size: 40,
              color: color,
            ),
            SizedBox(height: 10),
            Text(
              title,
              style: TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w600,
                color: Colors.blueGrey[800],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
