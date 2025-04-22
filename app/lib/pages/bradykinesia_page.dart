import 'package:flutter/material.dart';

class BradykinesiaPage extends StatelessWidget {
  const BradykinesiaPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Bradykinesia Test'),
        backgroundColor: Colors.indigo,
      ),
      body: const Center(
        child: Text(
          'Bradykinesia Test Page - Coming Soon',
          style: TextStyle(fontSize: 20),
        ),
      ),
    );
  }
} 