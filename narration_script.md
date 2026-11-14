# Naskah Narasi — Dynamic Programming: Maximum Subarray Sum (Session 15)

- **Bahasa:** Indonesia (istilah teknis CS tetap dalam bahasa Inggris)
- **Voice TTS:** `id-ID-ArdiNeural` (Microsoft Edge Neural TTS), rate `-3%`
- **Jumlah scene:** 14  ·  **Jumlah segment:** 63
- **Total durasi narasi:** 17.7 menit

> File ini di-generate otomatis dari `manim/narration.py` (sumber kebenaran). Untuk mengubah narasi, edit `manim/narration.py`, lalu jalankan ulang `./render_preview.sh` / `./render_final.sh`.

## 1. Pembukaan, Learning Outcomes, dan Outline

*Scene Manim:* `S01Intro`

**[s01_title · 18.7 s]**

Halo semuanya, selamat datang di Session 15. Hari ini kita akan membahas salah satu teknik desain algoritma yang paling sering muncul, baik di perkuliahan, di technical interview, maupun di competitive programming, yaitu Dynamic Programming. Studi kasus utama kita adalah Maximum Subarray Sum.

**[s01_lo2 · 18.8 s]**

Ada dua learning outcome yang ingin kita capai. Pertama, LO 2: kalian mampu mengidentifikasi optimal substructure dan overlapping subproblems sebagai syarat penerapan DP. Kalian juga bisa membedakan DP dari greedy dan divide and conquer, serta menjelaskan kenapa algoritma Kadane termasuk DP.

**[s01_lo3 · 20.0 s]**

Kedua, LO 3: kalian mampu mendesain algoritma Kadane dengan recurrence dp[i] = max(A[i], dp[i-1] + A[i]). Caranya dengan menerapkan empat langkah desain DP, yaitu characterize, define, compute, dan construct, lalu mengimplementasikannya dengan memoization maupun tabulation.

**[s01_outline · 21.2 s]**

Alurnya begini. Kita mulai dari paradigma DP, yaitu optimal substructure dan overlapping subproblems. Lalu kita bandingkan memoization dengan tabulation. Setelah itu kita masuk ke Maximum Subarray Sum dengan algoritma Kadane. Dan terakhir, kita diskusikan kenapa Kadane itu DP, dan bukan greedy.

## 2. Why DP? Recursion Tree Fibonacci

*Scene Manim:* `S02WhyDP`

**[s02_code · 16.9 s]**

Kita mulai dengan satu latihan sederhana. Coba hitung fib(5) secara rekursif. Ini pseudocode-nya. Kalau n kurang dari atau sama dengan 1, kembalikan n. Kalau tidak, kembalikan FIB(n-1) + FIB(n-2).

**[s02_tree · 14.3 s]**

Sekarang kita gambar recursion tree-nya. fib(5) memanggil fib(4) dan fib(3). fib(4) memanggil fib(3) dan fib(2), dan seterusnya, sampai semua cabang berhenti di base case, yaitu fib(1) dan fib(0).

**[s02_question · 15.3 s]**

Pertanyaannya, berapa kali kita menghitung fib(2)? Perhatikan lingkaran merah. Ternyata fib(2) dihitung sebanyak tiga kali. Bagaimana dengan fib(3)? Lingkaran biru menunjukkan fib(3) dihitung dua kali.

**[s02_problem · 17.4 s]**

Inilah sumber masalahnya. Subproblem yang sama muncul lagi dan lagi. Semakin besar n, pengulangan ini meledak secara eksponensial, sehingga kompleksitasnya menjadi O(2^n). Nah, bagaimana kalau hasilnya kita catat pada saat pertama kali dihitung?

## 3. Memoization pada Fibonacci

*Scene Manim:* `S03Memoization`

**[s03_code1 · 12.7 s]**

Itulah ide dari memoization. Perhatikan pseudocode MEMOIZED-FIB. Kita siapkan sebuah array memo dari 0 sampai n, lalu semua isinya kita set NIL, yang artinya belum pernah dihitung.

**[s03_code2 · 18.7 s]**

Di fungsi MEMOIZED-FIB-AUX, setelah base case, kita cek dulu. Kalau memo[n] tidak NIL, berarti nilainya sudah tersimpan, jadi langsung kembalikan saja, tidak perlu dihitung ulang. Kalau belum, kita hitung secara rekursif, simpan hasilnya ke memo[n], baru kemudian dikembalikan.

**[s03_trace · 16.9 s]**

Mari kita lihat efeknya. Pemanggilan pertama turun di sepanjang cabang kiri, dari fib(5), fib(4), fib(3), fib(2), sampai fib(1) dan fib(0). Setiap kali sebuah nilai selesai dihitung, nilai itu langsung disimpan ke dalam array memo.

**[s03_hit · 14.5 s]**

Ketika fib(4) membutuhkan fib(2), dan fib(5) membutuhkan fib(3), nilainya sudah ada di memo. Jadi subproblem yang sama memang tetap dipanggil, tetapi tidak dihitung lebih jauh. Recursion tree-nya menyusut drastis.

**[s03_complexity · 7.4 s]**

Karena setiap subproblem diselesaikan paling banyak satu kali, kompleksitas waktunya turun dari O(2^n) menjadi O(n).

## 4. Definisi Dynamic Programming

*Scene Manim:* `S04Definition`

**[s04_def · 11.6 s]**

Sekarang kita formalkan. Dynamic Programming adalah teknik desain algoritma untuk menyelesaikan masalah yang memiliki overlapping subproblems dan optimal substructure, dengan cara menyimpan hasil antara.

**[s04_props · 21.4 s]**

Jadi, DP bisa diterapkan kalau dua syarat terpenuhi. Pertama, optimal substructure: solusi optimal dari sebuah masalah mengandung solusi optimal dari subproblem-subproblem-nya. Kedua, overlapping subproblems: subproblem yang sama diselesaikan berulang kali dalam solusi rekursif yang naif, persis seperti fib(2) dan fib(3) tadi.

**[s04_contrast · 16.5 s]**

Ini berbeda dengan Divide and Conquer, yang subproblem-nya saling independen dan tidak tumpang tindih. DP juga berbeda dengan Greedy. Greedy memang memiliki optimal substructure, tetapi hanya mengambil satu pilihan greedy di setiap langkah, tanpa mengevaluasi ulang.

## 5. Top-down (Memoization) vs Bottom-up (Tabulation)

*Scene Manim:* `S05TopDownBottomUp`

**[s05_two · 19.3 s]**

Ada dua cara mengimplementasikan DP. Yang pertama top-down, atau memoization: kita tulis rekursi yang natural, lalu cache hasilnya supaya tidak dihitung ulang. Yang kedua bottom-up, atau tabulation: kita isi sebuah tabel dengan urutan yang menjamin setiap subproblem sudah diselesaikan sebelum dibutuhkan.

**[s05_question · 7.7 s]**

MEMOIZED-FIB yang tadi adalah contoh implementasi top-down. Pertanyaannya, bisakah kita mengubahnya menjadi bottom-up?

**[s05_code · 20.2 s]**

Tentu bisa. Ini FIB-DP. Kita buat array dp dari 0 sampai n, lalu isi dp[0] = 0 dan dp[1] = 1. Kemudian untuk i dari 2 sampai n, dp[i] = dp[i-1] + dp[i-2]. Terakhir, kembalikan dp[n].

**[s05_fill · 19.0 s]**

Perhatikan arah pengisiannya, dari kiri ke kanan. dp[2] = 1, dp[3] = 2, dp[4] = 3, dan dp[5] = 5. Tidak ada rekursi sama sekali. Cukup satu loop, sehingga kompleksitas waktunya juga O(n).

**[s05_table · 24.6 s]**

Lalu apa bedanya? Dari sisi komputasi, memoization hanya menghitung subproblem yang benar-benar dibutuhkan, sedangkan tabulation menghitung semua subproblem. Dari sisi space, memoization butuh space sebesar jumlah subproblem yang dihitung, sedangkan tabulation sebesar ukuran tabel. Dan dari sisi overhead, memoization terbebani oleh rekursi, sementara tabulation cukup dengan iterasi.

## 6. Empat Langkah Desain DP

*Scene Manim:* `S06DesignSteps`

**[s06_steps · 26.7 s]**

Secara umum, ada empat langkah untuk mendesain algoritma DP. Satu, characterize: pahami struktur dari solusi optimal. Dua, define: definisikan nilai solusi optimal secara rekursif. Tiga, compute: hitung nilainya secara bottom-up, atau top-down dengan memoization. Empat, construct: bangun solusi optimalnya dari informasi yang sudah dihitung.

**[s06_apply · 5.0 s]**

Keempat langkah ini akan kita pakai satu per satu untuk menyelesaikan masalah utama kita hari ini.

## 7. Maximum Subarray Sum: Problem

*Scene Manim:* `S07Problem`

**[s07_statement · 15.9 s]**

Masalahnya begini. Diberikan sebuah array A dari 1 sampai n berisi bilangan bulat, yang bisa saja negatif. Cari subarray yang contiguous, artinya elemennya berurutan tanpa melompat, yaitu A[i..j], yang jumlahnya paling besar.

**[s07_example · 16.6 s]**

Contohnya array ini: -2, 1, -3, 4, -1, 2, 1, -5, 4. Jawabannya adalah A[4..7], yaitu 4, -1, 2, 1, dengan jumlah 6.

**[s07_insight · 14.2 s]**

Perhatikan, subarray terbaik ini justru mengandung -1. Jadi kita tidak bisa sekadar mengambil angka positif saja. Kadang, menelan angka negatif itu menguntungkan, asalkan setelahnya ada angka positif yang lebih besar.

## 8. Naive Approach dan Overlapping Subproblems

*Scene Manim:* `S08Naive`

**[s08_enum · 16.1 s]**

Pendekatan paling naif adalah mencoba semua kemungkinan. Untuk setiap index i, ada tepat i subarray yang berakhir di index tersebut. Di index 1 hanya ada satu, di index 2 ada dua, di index 3 ada tiga, dan seterusnya sampai index n.

**[s08_count · 13.5 s]**

Jadi total ada 1 + 2 + 3 + ... + n, atau O(n²) subarray. Untuk setiap subarray, menghitung jumlahnya butuh O(n). Total kompleksitasnya menjadi O(n³).

**[s08_code · 18.4 s]**

Ini pseudocode BRUTE-FORCE-SUM. Loop pertama memilih end index, loop kedua mencari setiap kemungkinan start index, dan loop ketiga menjumlahkan elemen dari start sampai end. Setiap hasilnya dibandingkan dengan global_max. Tiga loop bersarang, itulah sumber O(n³).

**[s08_overlap · 19.9 s]**

Sekarang perhatikan baik-baik. Saat i = 2, kita menjumlahkan A[1] dan A[2]. Saat i = 3, kita kembali menjumlahkan A[1] dan A[2], baru kemudian menambahkan A[3]. Bagian yang sama dihitung berulang kali. Overlapping subproblems terjadi di mana-mana.

**[s08_idea · 10.9 s]**

Kalau dilihat lebih dekat, sebenarnya kita hanya peduli pada jumlah maksimum yang berakhir di index sebelumnya. Jadi, bagaimana kalau kita simpan jumlah maksimum untuk setiap ending index?

## 9. Step 1 & Step 2: Characterize dan Define

*Scene Manim:* `S09Characterize`

**[s09_def · 9.6 s]**

Inilah langkah pertama, characterize. Kita definisikan subproblem-nya: dp[i] adalah jumlah subarray maksimum yang berakhir tepat di index i.

**[s09_options · 17.8 s]**

Subarray optimal yang berakhir di index i hanya punya dua pilihan struktural. Opsi A, extend: lanjutkan subarray optimal yang berakhir di i-1, lalu tambahkan A[i]. Opsi B, start: mulai subarray yang benar-benar baru di index i, kalau opsi A memberikan nilai yang lebih kecil.

**[s09_theorem · 10.6 s]**

Dari sini kita mendapatkan teoremanya: solusi optimal untuk subproblem di index i mengandung solusi optimal untuk subproblem di index i-1. Itulah optimal substructure.

**[s09_recurrence · 13.1 s]**

Langkah kedua, define. Dua opsi tadi langsung kita tulis sebagai recurrence: dp[i] = max(A[i], dp[i-1] + A[i]). Suku pertama adalah opsi start, suku kedua adalah opsi extend.

**[s09_base · 16.7 s]**

Base case-nya, kita tidak bisa melihat ke belakang sebelum elemen pertama, jadi dp[1] = A[1]. Dan karena subarray maksimum bisa berakhir di mana saja, jawaban akhirnya adalah GlobalMax, yaitu nilai maksimum dari semua dp[i], untuk i dari 1 sampai n.

## 10. Step 3: Compute Bottom-up

*Scene Manim:* `S10Compute`

**[s10_code · 17.0 s]**

Langkah ketiga, compute. Ini KADANE-TABLE. Kita isi dp[1] dengan A[1], dan global_max juga A[1]. Lalu untuk i dari 2 sampai n, hitung dp[i] dengan recurrence tadi, dan perbarui global_max kalau dp[i] lebih besar.

**[s10_fill1 · 19.7 s]**

Mari kita jalankan pada contoh kita. dp[1] = -2. dp[2] = max(1, -2 + 1) = 1, artinya kita mulai baru. dp[3] = max(-3, 1 + (-3)) = -2, artinya kita extend.

**[s10_fill2 · 23.8 s]**

dp[4] = max(4, -2 + 4) = 4, mulai baru lagi. Lalu kita terus extend: dp[5] = 3, dp[6] = 5, dan dp[7] = 6. Kemudian dp[8] = 1, dan dp[9] = 5. Nilai maksimum di tabel adalah 6, sesuai dengan jawaban kita.

**[s10_observe · 11.8 s]**

Perhatikan, untuk menghitung dp[i], kita hanya pernah melihat dp[i-1]. Jadi seluruh array sebenarnya tidak perlu disimpan. Cukup satu variabel untuk melacak state.

**[s10_space · 17.5 s]**

Hasilnya adalah KADANE-SPACE-OPTIMIZED. Array dp diganti dengan satu variabel, curr_max. Dengan begitu, space complexity turun dari O(n) menjadi O(1), sementara waktunya tetap O(n). Pelajaran pentingnya: algoritma DP tidak selalu tentang tabel.

**[s10_fib · 11.7 s]**

Sebenarnya, kalian mungkin sudah pernah melakukan trik ini di Fibonacci. FIB-SPACE-OPTIMIZED hanya menyimpan dua nilai terakhir, prev1 dan prev2, lalu menggesernya di setiap iterasi.

## 11. Step 4: Construct the Solution

*Scene Manim:* `S11Construct`

**[s11_question · 14.9 s]**

Sekarang kita sudah punya nilai optimalnya. Tapi bagaimana kalau kita ingin tahu, subarray mana yang menghasilkan nilai itu? Untuk itu kita butuh informasi index. Jadi, kita lacak batas index setiap kali nilainya berubah.

**[s11_rules · 13.6 s]**

Ada dua aturan. Expansion rule: kalau curr_max di-reset, batas awal bergeser ke index saat ini. Global rule: kalau tercapai global maximum yang baru, simpan batas start dan end secara permanen.

**[s11_code · 19.2 s]**

Ini KADANE-CONSTRUCT. Kita tambahkan tiga variabel: start, end, dan temp_start. Saat A[i] lebih besar dari curr_max + A[i], kita reset, dan temp_start menjadi i. Saat curr_max melampaui global_max, start diisi dengan temp_start, dan end diisi dengan i.

**[s11_init · 14.3 s]**

Mari kita trace pada array -2, 1, -3, 4, -1, 2, 1. Inisialisasi: curr_max dan global_max sama-sama -2, dan subarray-nya hanya -2.

**[s11_i23 · 20.3 s]**

i = 2: max(1, -2 + 1) = 1. Ini reset, temp_start pindah ke 2, dan global_max naik menjadi 1. i = 3: max(-3, 1 + (-3)) = -2. Kita extend, tapi global_max tetap 1.

**[s11_i45 · 15.9 s]**

i = 4: max(4, -2 + 4) = 4. Reset lagi, temp_start pindah ke 4, dan global_max naik menjadi 4. i = 5: curr_max menjadi 3, sedangkan global_max tetap 4.

**[s11_i67 · 20.5 s]**

i = 6: curr_max menjadi 5, dan global_max ikut naik. Terakhir i = 7: curr_max menjadi 6, dan global_max naik menjadi 6. Jadi start = 4, end = 7, dan subarray-nya adalah 4, -1, 2, 1, dengan jumlah 6.

## 12. Why Kadane's is DP and Not Greedy

*Scene Manim:* `S12WhyNotGreedy`

**[s12_props · 21.2 s]**

Sekarang pertanyaan terakhir: kenapa Kadane itu DP, dan bukan greedy? Pertama, Kadane memenuhi kedua properti DP. Optimal substructure: subarray optimal yang berakhir di i adalah A[i] sendirian, atau A[i] yang ditempelkan ke subarray optimal yang berakhir di i-1. Solusi subproblem-nya dipakai secara langsung.

**[s12_overlap · 15.7 s]**

Overlapping subproblems: kalau untuk setiap i kita bertanya, berapa subarray terbaik yang berakhir di i, lalu menghitungnya dari nol setiap kali, kita akan memeriksa prefix yang sama berulang-ulang. DP menghindari hal itu dengan dp[i-1], atau curr_max.

**[s12_greedy · 16.3 s]**

Algoritma greedy akan melakukan satu kali pass dengan aturan yang tetap. Misalnya aturannya: ambil elemen selama positif, dan reset ketika bertemu angka negatif. Coba kita jalankan pada A = -1, 3, -1, 4.

**[s12_fail · 17.6 s]**

Greedy mengambil 3, lalu bertemu -1 di index 3 dan langsung reset. Setelah itu ia mengambil 4. Hasil terbaiknya hanya 4. Padahal subarray 3, -1, 4 memberikan jumlah 6. Greedy melewatkannya.

**[s12_kadane · 26.9 s]**

Kadane berbeda. Di index 3, curr_max = 3 + (-1) = 2, masih lebih baik daripada mulai baru dari -1, jadi ia extend. Di index 4, 2 + 4 = 6. Kadane membuat keputusan di setiap langkah, extend atau restart, berdasarkan state yang sudah dihitung sebelumnya, yaitu dp[i-1]. Itu adalah keputusan DP, bukan pilihan greedy.

**[s12_table · 23.3 s]**

Ringkasnya begini. Greedy memutuskan hanya dari input mentah atau heuristik di langkah saat ini, sedangkan DP memakai state subproblem yang sudah dihitung. Greedy memilih sebelum menyelesaikan subproblem, sementara DP memilih setelah mengevaluasi subproblem sebelumnya. Greedy tidak pernah melihat ke belakang, sedangkan DP justru harus membaca tabel atau state yang sudah diselesaikan.

**[s12_examples · 14.1 s]**

Contoh algoritma greedy adalah Activity Selection, Fractional Knapsack, Huffman Code, dan Dijkstra. Sedangkan contoh DP adalah Max Subarray Sum, 0/1 Knapsack, dan Coin Change untuk sistem koin yang non-canonical.

## 13. Summary

*Scene Manim:* `S13Summary`

**[s13_a · 19.6 s]**

Mari kita rangkum. Satu, DP menyelesaikan masalah dengan meng-cache solusi dari overlapping subproblems, dan membutuhkan optimal substructure. Dua, memoization bersifat top-down, yaitu meng-cache pemanggilan rekursif, sedangkan tabulation bersifat bottom-up, yaitu mengisi tabel secara iteratif.

**[s13_b · 20.6 s]**

Tiga, algoritma Kadane: dp[i] = max(A[i], dp[i-1] + A[i]), dengan waktu O(n), dan space O(1) pada versi yang dioptimasi. Empat, Kadane adalah DP karena setiap dp[i] bergantung pada dp[i-1], dan keputusannya tidak bisa dibuat secara greedy tanpa mengetahui state optimal sebelumnya.

## 14. Exercise dan References

*Scene Manim:* `S14Exercise`

**[s14_stairs · 26.3 s]**

Sebelum kita tutup, ada dua latihan untuk kalian. Latihan pertama, Climbing Stairs. Ada sebuah tangga dengan n anak tangga. Setiap kali melangkah, kalian boleh naik 1 atau 2 anak tangga. Berapa banyak cara berbeda untuk sampai ke puncak? Contohnya, untuk n = 3 jawabannya 3, yaitu 1+1+1, 1+2, atau 2+1.

**[s14_stairs_task · 13.8 s]**

Tugas kalian: tuliskan pseudocode-nya dengan pendekatan DP menggunakan empat langkah tadi. Petunjuknya, pikirkan dari anak tangga mana saja kalian bisa sampai ke anak tangga terakhir. Mungkin polanya akan terasa familiar.

**[s14_product · 18.3 s]**

Latihan kedua, Maximum Product Subarray. Cari subarray contiguous yang hasil kalinya paling besar. Contohnya, untuk A = -1, 3, -4, -2, jawabannya 24, dari subarray 3, -4, -2.

**[s14_product_task · 14.1 s]**

Pertanyaannya, kenapa algoritma Kadane yang standar tidak berhasil di sini? Bagaimana cara membuatnya berhasil, dan kenapa? Petunjuknya, perhatikan apa yang terjadi ketika bilangan negatif dikalikan dengan bilangan negatif.

**[s14_refs · 16.1 s]**

Referensi untuk sesi ini adalah Cormen dan kawan-kawan, Introduction to Algorithms edisi keempat, bab 14.3, dan Skiena, The Algorithm Design Manual edisi ketiga, bab 10.1. Terima kasih, dan sampai jumpa di sesi berikutnya!
