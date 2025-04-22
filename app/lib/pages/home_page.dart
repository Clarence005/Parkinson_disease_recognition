import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'spiral_page.dart';
import 'gait_page.dart';
import 'bradykinesia_page.dart';
import 'tremor_page.dart';
import 'history_page.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ParkinScan',style: TextStyle(color: Colors.white),),
        backgroundColor: Colors.indigo,
      ),
      drawer: Drawer(

        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            const DrawerHeader(
              decoration: BoxDecoration(
                color: Colors.indigo,
              ),
              child: Text(
                'ParkinScan',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                ),
              ),
            ),
            ListTile(
              leading: const Icon(Icons.home),
              title: const Text('Home'),
              onTap: () {
                Navigator.pop(context);
              },
            ),
            ListTile(
              leading: const Icon(Icons.spatial_audio_off),
              title: const Text('Spiral Test'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const SpiralPage()),
                );
              },
            ),
            ListTile(
              leading: const Icon(Icons.directions_walk),
              title: const Text('Gait Analysis'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const GaitPage()),
                );
              },
            ),
            ListTile(
              leading: const Icon(Icons.timer),
              title: const Text('Bradykinesia Test'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const BradykinesiaPage()),
                );
              },
            ),
            ListTile(
              leading: const Icon(Icons.vibration),
              title: const Text('Tremor Analysis'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const TremorPage()),
                );
              },
            ),
            ListTile(
              leading: const Icon(Icons.history),
              title: const Text('Test History'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const HistoryPage()),
                );
              },
            ),
          ],
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Parkinson\'s Disease',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.indigo,
              ),
            ),
            const SizedBox(height: 20),
            const Text(
              'Parkinson\'s disease is a progressive neurological disorder that affects movement. It develops gradually, sometimes starting with a barely noticeable tremor in just one hand. While tremors are common, the disorder also commonly causes stiffness or slowing of movement.',
              style: TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 20),
            const Text(
              'Early Detection Using MDS-UPDRS',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.indigo,
              ),
            ),
            const SizedBox(height: 10),
            const Text(
              'Our application uses the Movement Disorder Society Unified Parkinson\'s Disease Rating Scale (MDS-UPDRS) to help in early detection of Parkinson\'s disease through the following symptoms:',
              style: TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 10),
            _buildSymptomCard(
              'Spiral Drawing',
              'Analyzing spiral drawings for signs of bradykinesia and tremors',
              Icons.spatial_audio_off,
            ),
            _buildSymptomCard(
              'Gait Analysis',
              'Evaluating walking patterns for inconsistencies and freezing',
              Icons.directions_walk,
            ),
            _buildSymptomCard(
              'Bradykinesia',
              'Measuring slowness of movement and reduced amplitude',
              Icons.timer,
            ),
            _buildSymptomCard(
              'Rest Tremors',
              'Detecting involuntary shaking movements at rest',
              Icons.vibration,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSymptomCard(String title, String description, IconData icon) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8.0),
      child: ListTile(
        leading: Icon(icon, color: Colors.indigo),
        title: Text(
          title,
          style: const TextStyle(
            fontWeight: FontWeight.bold,
            color: Colors.indigo,
          ),
        ),
        subtitle: Text(description),
      ),
    );
  }
} 