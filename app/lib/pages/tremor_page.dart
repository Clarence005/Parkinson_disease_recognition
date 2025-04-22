import 'package:flutter/material.dart';

class TremorPage extends StatelessWidget {
  const TremorPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tremor Analysis'),
        backgroundColor: Colors.indigo,
      ),
      body: const Center(
        child: Text(
          'Tremor Analysis Page - Coming Soon',
          style: TextStyle(fontSize: 20),
        ),
      ),
    );
  }
} 