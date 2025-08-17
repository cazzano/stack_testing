import 'package:flutter/material.dart';

class SkillsPage extends StatelessWidget {
  final List<Skill> skills = [
    Skill('Flutter', 0.9, Colors.blue),
    Skill('Dart', 0.85, Colors.cyan),
    Skill('JavaScript', 0.8, Colors.yellow),
    Skill('Python', 0.75, Colors.green),
    Skill('React', 0.7, Colors.blue[300]!),
    Skill('Node.js', 0.65, Colors.green[700]!),
    Skill('Firebase', 0.8, Colors.orange),
    Skill('Git', 0.85, Colors.red),
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
            'My Skills',
            style: TextStyle(
              fontSize: 28,
              fontWeight: FontWeight.bold,
              color: Colors.blueGrey[800],
            ),
          ),
          SizedBox(height: 10),
          Text(
            'Here are the technologies and tools I work with:',
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
              crossAxisCount: MediaQuery.of(context).size.width > 600 ? 2 : 1,
              childAspectRatio: 4,
              crossAxisSpacing: 20,
              mainAxisSpacing: 20,
            ),
            itemCount: skills.length,
            itemBuilder: (context, index) {
              return _buildSkillCard(skills[index]);
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
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Other Skills',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Colors.blueGrey[800],
                  ),
                ),
                SizedBox(height: 15),
                Wrap(
                  spacing: 10,
                  runSpacing: 10,
                  children: [
                    _buildSkillChip('UI/UX Design'),
                    _buildSkillChip('API Integration'),
                    _buildSkillChip('Database Design'),
                    _buildSkillChip('Version Control'),
                    _buildSkillChip('Agile Development'),
                    _buildSkillChip('Testing'),
                    _buildSkillChip('Deployment'),
                    _buildSkillChip('Problem Solving'),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSkillCard(Skill skill) {
    return Container(
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
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                skill.name,
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.blueGrey[800],
                ),
              ),
              Text(
                '${(skill.level * 100).round()}%',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                  color: skill.color,
                ),
              ),
            ],
          ),
          SizedBox(height: 10),
          LinearProgressIndicator(
            value: skill.level,
            backgroundColor: Colors.grey[300],
            valueColor: AlwaysStoppedAnimation<Color>(skill.color),
            minHeight: 8,
          ),
        ],
      ),
    );
  }

  Widget _buildSkillChip(String skill) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: Colors.blueGrey[100],
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.blueGrey[300]!),
      ),
      child: Text(
        skill,
        style: TextStyle(
          color: Colors.blueGrey[700],
          fontSize: 12,
          fontWeight: FontWeight.w500,
        ),
      ),
    );
  }
}

class Skill {
  final String name;
  final double level;
  final Color color;

  Skill(this.name, this.level, this.color);
}
