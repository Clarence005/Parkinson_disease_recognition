import 'package:flutter/material.dart';

class GaitPage extends StatelessWidget {
  const GaitPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Gait Analysis'),
        backgroundColor: Colors.indigo,
      ),
      body: const Center(
        child: Text(
          'Gait Analysis Page - Coming Soon',
          style: TextStyle(fontSize: 20),
        ),
      ),
    );
  }
} 