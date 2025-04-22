import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';

class HistoryPage extends StatelessWidget {
  const HistoryPage({super.key});

  @override
  Widget build(BuildContext context) {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) {
      return const Scaffold(
        body: Center(
          child: Text('Please log in to view history'),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Test History', style: TextStyle(color: Colors.white)),
        backgroundColor: Colors.indigo,
      ),
      body: StreamBuilder<QuerySnapshot>(
        stream: FirebaseFirestore.instance
            .collection('spiral_analyses')
            .where('userId', isEqualTo: user.uid)
            .orderBy('timestamp', descending: true)
            .snapshots(),
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }

          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          final analyses = snapshot.data?.docs ?? [];

          if (analyses.isEmpty) {
            return const Center(child: Text('No test history available'));
          }

          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: analyses.length,
            itemBuilder: (context, index) {
              final analysis = analyses[index].data() as Map<String, dynamic>;
              final timestamp = (analysis['timestamp'] as Timestamp).toDate();
              final result = analysis['result'] as String;
              final confidence = analysis['confidence'] as double;

              return Card(
                margin: const EdgeInsets.only(bottom: 16),
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Test Date: ${timestamp.toString().split('.')[0]}',
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'Result: ${result == 'patient' ? 'Signs of Parkinsons detected' : 'No signs of Parkinsons detected'}',
                        style: TextStyle(
                          color: result == 'patient' ? Colors.red : Colors.green,
                          fontSize: 16,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'Confidence: ${(confidence * 100).toStringAsFixed(2)}%',
                        style: const TextStyle(fontSize: 14),
                      ),
                    ],
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}