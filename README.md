# Algeo02-21041 - HananGeming
Eigen Values and EigenFace Application for Face Recognition 
> IF2123 Geometry and Linear Algebra 2022/2023 Project 2

## Screenshot
![alt text](doc/screenshot.png)

## Deskripsi
Pengenalan wajah (Face Recognition) adalah teknologi biometrik yang bisa dipakai untuk mengidentifikasi wajah seseorang untuk berbagai kepentingan khususnya keamanan. Program pengenalan wajah melibatkan kumpulan citra wajah yang sudah disimpan pada database lalu berdasarkan kumpulan citra wajah tersebut, program dapat mempelajari bentuk wajah lalu mencocokkan antara kumpulan citra wajah yang sudah dipelajari dengan citra yang akan diidentifikasi.

Terdapat berbagai teknik untuk memeriksa citra wajah dari kumpulan citra yang sudah diketahui seperti jarak Euclidean dan cosine similarity, principal component analysis (PCA), serta Eigenface. Pada Tugas ini, akan dibuat sebuah program pengenalan wajah menggunakan Eigenface.

## Anggota Kelompok - HananGeming
|NIM|Nama|
|----------|-------------------------|
| 13521041 | Muhammad Hanan          |
| 13521081 | Bagas Aryo Seto         |
| 13521106 | Mohammad Farhan Fahrezy |

## Teknologi yang digunakan
- tkinter
- cv2
- PIL
- numpy

## Cara Penggunaan
1. Pastikan semua teknologi yang digunakan sudah terinstall
2. Pada folder `\src` jalankan script `python mainwindows.py`.
    ```
    python mainwindows.py
    ```
3. Pilih dataset dan test-image yang ingin digunakan
4. tekan `Start` untuk memulai proses face recognition 