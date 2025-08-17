import 'package:flutter/material.dart';

class AppLayout extends StatelessWidget {
  final Widget child;

  const AppLayout({Key? key, required this.child}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'My Portfolio',
          style: TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 24,
          ),
        ),
        backgroundColor: Colors.blueGrey[800],
        foregroundColor: Colors.white,
        elevation: 0,
        centerTitle: false,
        actions: [
          _buildNavButton(context, 'Home', '/'),
          _buildNavButton(context, 'Skills', '/skills'),
          _buildNavButton(context, 'Projects', '/projects'),
          _buildNavButton(context, 'Contact', '/contact'),
          SizedBox(width: 16),
        ],
      ),
      body: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Colors.blueGrey[50]!,
              Colors.grey[100]!,
            ],
          ),
        ),
        child: child,
      ),
      bottomNavigationBar: Container(
        height: 80,
        decoration: BoxDecoration(
          color: Colors.blueGrey[800],
          boxShadow: [
            BoxShadow(
              color: Colors.black26,
              blurRadius: 10,
              offset: Offset(0, -2),
            ),
          ],
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            _buildFooterNavButton(context, Icons.home, 'Home', '/'),
            _buildFooterNavButton(context, Icons.build, 'Skills', '/skills'),
            _buildFooterNavButton(context, Icons.work, 'Projects', '/projects'),
            _buildFooterNavButton(context, Icons.contact_mail, 'Contact', '/contact'),
          ],
        ),
      ),
    );
  }

  Widget _buildNavButton(BuildContext context, String title, String route) {
    bool isActive = ModalRoute.of(context)?.settings.name == route;
    
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 8),
      child: TextButton(
        onPressed: () {
          Navigator.pushReplacementNamed(context, route);
        },
        style: TextButton.styleFrom(
          foregroundColor: isActive ? Colors.yellow : Colors.white,
          backgroundColor: isActive ? Colors.black26 : Colors.transparent,
          padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
          ),
        ),
        child: Text(
          title,
          style: TextStyle(
            fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
            fontSize: 16,
          ),
        ),
      ),
    );
  }

  Widget _buildFooterNavButton(BuildContext context, IconData icon, String title, String route) {
    bool isActive = ModalRoute.of(context)?.settings.name == route;
    
    return InkWell(
      onTap: () {
        Navigator.pushReplacementNamed(context, route);
      },
      child: Container(
        padding: EdgeInsets.symmetric(vertical: 12),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              color: isActive ? Colors.yellow : Colors.white70,
              size: 24,
            ),
            SizedBox(height: 4),
            Text(
              title,
              style: TextStyle(
                color: isActive ? Colors.yellow : Colors.white70,
                fontSize: 12,
                fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
