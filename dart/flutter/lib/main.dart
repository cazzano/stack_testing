import 'package:flutter/material.dart';
import 'layout.dart';
import 'pages/home.dart';
import 'pages/skills.dart';
import 'pages/projects.dart';
import 'pages/contact.dart';

void main() {
  runApp(PortfolioApp());
}

class PortfolioApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My Portfolio',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
        fontFamily: 'Arial',
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => AppLayout(child: HomePage()),
        '/skills': (context) => AppLayout(child: SkillsPage()),
        '/projects': (context) => AppLayout(child: ProjectsPage()),
        '/contact': (context) => AppLayout(child: ContactPage()),
      },
    );
  }
}
