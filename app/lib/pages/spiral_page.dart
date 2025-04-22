import 'dart:convert';
import 'package:http_parser/http_parser.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:path/path.dart' as path;
import 'package:mime/mime.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:fl_chart/fl_chart.dart';

class SpiralPage extends StatefulWidget {
  const SpiralPage({super.key});

  @override
  State<SpiralPage> createState() => _SpiralPageState();
}

class _SpiralPageState extends State<SpiralPage> {
  final ImagePicker _picker = ImagePicker();
  File? _image;
  bool _isLoading = false;
  String? _analysisResult;
  double? _confidence;

  Future<void> _pickImage() async {
    try {
      final XFile? pickedFile =
      await _picker.pickImage(source: ImageSource.gallery);
      if (pickedFile != null) {
        setState(() {
          _image = File(pickedFile.path);
          _analysisResult = null;
          _confidence = null;
        });
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error picking image: $e')),
      );
    }
  }

  Future<void> _uploadAndAnalyzeImage() async {
    if (_image == null) return;

    setState(() => _isLoading = true);

    try {
      final user = FirebaseAuth.instance.currentUser;
      if (user == null) throw Exception('User not logged in');

      final uri = Uri.parse("http://192.168.165.72:5000/predict"); // Replace with your local IP or public URL
      final request = http.MultipartRequest('POST', uri);

      final mimeType = lookupMimeType(_image!.path) ?? 'image/jpeg';

      request.files.add(await http.MultipartFile.fromPath(
        'file',
        _image!.path,
        contentType: MediaType.parse(mimeType),
      ));

      final response = await request.send();

      if (response.statusCode != 200) {
        throw Exception('Failed to get prediction');
      }

      final responseBody = await response.stream.bytesToString();
      final resultData = jsonDecode(responseBody);

      final result = resultData['class_name']; // "healthy" or "patient"
      final confidence = resultData['confidence']; // e.g., 0.85

      await FirebaseFirestore.instance.collection('spiral_analyses').add({
        'userId': user.uid,
        'timestamp': DateTime.now(),
        'result': result,
        'confidence': confidence,
      });

      setState(() {
        _analysisResult = result;
        _confidence = confidence;
        _isLoading = false;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Analysis completed successfully')),
      );
    } catch (e) {
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Spiral Test',style:TextStyle(color:Colors.white)),
        backgroundColor: Colors.indigo,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text(
                'Upload Spiral Drawing',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.indigo,
                ),
              ),
              const SizedBox(height: 20),
              const Text(
                'Please upload an image of your spiral drawing. The system will analyze it for signs of bradykinesia.',
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 20),
              if (_image != null)
                Container(
                  height: 300,
                  decoration: BoxDecoration(
                    border: Border.all(color: Colors.indigo),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Image.file(_image!, fit: BoxFit.contain),
                )
              else
                Container(
                  height: 300,
                  decoration: BoxDecoration(
                    border: Border.all(color: Colors.indigo),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Center(
                    child: Icon(
                      Icons.image,
                      size: 50,
                      color: Colors.indigo,
                    ),
                  ),
                ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _pickImage,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.indigo,
                  padding: const EdgeInsets.symmetric(vertical: 12),
                ),
                child: const Text('Select Image',style:TextStyle(color:Colors.white)),
              ),
              const SizedBox(height: 10),
              ElevatedButton(
                onPressed:
                _isLoading || _image == null ? null : _uploadAndAnalyzeImage,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.indigo,
                  padding: const EdgeInsets.symmetric(vertical: 12),
                ),
                child: _isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : const Text('Analyze Image',style:TextStyle(color:Colors.white)),
              ),
              if (_analysisResult != null) ...[
                const SizedBox(height: 20),
                Card(
                  color: _analysisResult == 'patient'
                      ? Colors.red.shade100
                      : Colors.green.shade100,
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      children: [
                        Text(
                          'Analysis Result:',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: _analysisResult == 'patient'
                                ? Colors.red
                                : Colors.green,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          _analysisResult == 'patient'
                              ? 'Signs of Parkinsons detected'
                              : 'No signs of Parkinsons detected',
                          style: const TextStyle(fontSize: 16),
                        ),
                        if (_confidence != null) ...[
                          const SizedBox(height: 8),
                          Text(
                            'Confidence: ${(_confidence! * 100).toStringAsFixed(2)}%',
                            style: const TextStyle(fontSize: 14),
                          ),
                          const SizedBox(height: 20),
                          SizedBox(
                            height: 250,
                            child: BarChart(
                              BarChartData(
                                alignment: BarChartAlignment.spaceAround,
                                maxY: 1.0,
                                barGroups: [
                                  BarChartGroupData(
                                    x: 0,
                                    barRods: [
                                      BarChartRodData(
                                        toY: _analysisResult == 'patient'
                                            ? _confidence!
                                            : 1 - _confidence!,
                                        color: Colors.red,
                                        width: 30,
                                        borderRadius: BorderRadius.circular(8),
                                        backDrawRodData: BackgroundBarChartRodData(
                                          show: true,
                                          toY: 1.0,
                                          color: Colors.grey.shade200,
                                        ),
                                      ),
                                    ],
                                  ),
                                  BarChartGroupData(
                                    x: 1,
                                    barRods: [
                                      BarChartRodData(
                                        toY: _analysisResult == 'patient'
                                            ? 1 - _confidence!
                                            : _confidence!,
                                        color: Colors.green,
                                        width: 30,
                                        borderRadius: BorderRadius.circular(8),
                                        backDrawRodData: BackgroundBarChartRodData(
                                          show: true,
                                          toY: 1.0,
                                          color: Colors.grey.shade200,
                                        ),
                                      ),
                                    ],
                                  ),
                                ],
                                titlesData: FlTitlesData(
                                  show: true,
                                  bottomTitles: AxisTitles(
                                    sideTitles: SideTitles(
                                      showTitles: true,
                                      getTitlesWidget: (value, meta) {
                                        switch (value.toInt()) {
                                          case 0:
                                            return const Padding(
                                              padding: EdgeInsets.only(top: 8.0),
                                              child: Text(
                                                "Parkinson's",
                                                style: TextStyle(
                                                  fontWeight: FontWeight.bold,
                                                  color: Colors.red,
                                                ),
                                              ),
                                            );
                                          case 1:
                                            return const Padding(
                                              padding: EdgeInsets.only(top: 8.0),
                                              child: Text(
                                                'Normal',
                                                style: TextStyle(
                                                  fontWeight: FontWeight.bold,
                                                  color: Colors.green,
                                                ),
                                              ),
                                            );
                                          default:
                                            return const Text('');
                                        }
                                      },
                                    ),
                                  ),
                                  leftTitles: AxisTitles(
                                    sideTitles: SideTitles(
                                      showTitles: true,
                                      reservedSize: 40,
                                      getTitlesWidget: (value, meta) {
                                        return Padding(
                                          padding: const EdgeInsets.only(right: 8.0),
                                          child: Text(
                                            '${(value * 100).toInt()}%',
                                            style: const TextStyle(
                                              fontWeight: FontWeight.bold,
                                              color: Colors.grey,
                                            ),
                                          ),
                                        );
                                      },
                                    ),
                                  ),
                                  rightTitles: AxisTitles(
                                    sideTitles: SideTitles(showTitles: false),
                                  ),
                                  topTitles: AxisTitles(
                                    sideTitles: SideTitles(showTitles: false),
                                  ),
                                ),
                                gridData: FlGridData(
                                  show: true,
                                  drawVerticalLine: false,
                                  horizontalInterval: 0.2,
                                  getDrawingHorizontalLine: (value) {
                                    return FlLine(
                                      color: Colors.grey.shade200,
                                      strokeWidth: 1,
                                    );
                                  },
                                ),
                                borderData: FlBorderData(
                                  show: true,
                                  border: Border(
                                    bottom: BorderSide(
                                      color: Colors.grey.shade300,
                                      width: 1,
                                    ),
                                    left: BorderSide(
                                      color: Colors.grey.shade300,
                                      width: 1,
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ),
                          const SizedBox(height: 16),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceAround,
                            children: [
                              _buildLegendItem(
                                'Parkinson\'s',
                                Colors.red,
                                _analysisResult == 'patient'
                                    ? _confidence!
                                    : 1 - _confidence!,
                              ),
                              _buildLegendItem(
                                'Normal',
                                Colors.green,
                                _analysisResult == 'patient'
                                    ? 1 - _confidence!
                                    : _confidence!,
                              ),
                            ],
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                Card(
                  color: Colors.blue.shade50,
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      children: [
                        if (_analysisResult == 'patient') ...[
                          if (_confidence! < 0.60)
                            const Text(
                              'Don\'t panic! The confidence level is below 60%. We recommend taking other tests for a more comprehensive assessment.',
                              style: TextStyle(
                                fontSize: 16,
                                color: Colors.blue,
                              ),
                              textAlign: TextAlign.center,
                            )
                          else
                            const Text(
                              'Based on the high confidence level, we recommend consulting a doctor for further evaluation.',
                              style: TextStyle(
                                fontSize: 16,
                                color: Colors.blue,
                              ),
                              textAlign: TextAlign.center,
                            ),
                        ] else ...[
                          if (_confidence! < 0.60)
                            const Text(
                              'The confidence level is below 60%. We recommend taking other tests for a more comprehensive assessment.',
                              style: TextStyle(
                                fontSize: 16,
                                color: Colors.blue,
                              ),
                              textAlign: TextAlign.center,
                            )
                          else
                            const Text(
                              'Great news! The test shows no signs of Parkinson\'s with high confidence. However, if you have concerns, we still recommend consulting a doctor.',
                              style: TextStyle(
                                fontSize: 16,
                                color: Colors.blue,
                              ),
                              textAlign: TextAlign.center,
                            ),
                        ],
                      ],
                    ),
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildLegendItem(String label, Color color, double value) {
    return Row(
      children: [
        Container(
          width: 16,
          height: 16,
          decoration: BoxDecoration(
            color: color,
            borderRadius: BorderRadius.circular(4),
          ),
        ),
        const SizedBox(width: 8),
        Text(
          '$label: ${(value * 100).toStringAsFixed(1)}%',
          style: const TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 14,
          ),
        ),
      ],
    );
  }
}
