"""Naskah narasi — SATU-SATUNYA sumber kebenaran untuk narasi, audio, dan caption.

Struktur:
    SCENES = [ { "scene": <nama class Manim>, "title": <judul>, "segments": [(segment_id, teks), ...] }, ... ]

* Setiap segment di-render menjadi satu file audio (audio/segments/<segment_id>.wav).
* Teks ditulis dalam bentuk yang enak dibaca sebagai caption (boleh memakai notasi
  seperti dp[i], A[i], O(n), -2). Konversi ke bentuk ucapan untuk TTS dilakukan oleh
  `to_speech()` di bawah, jadi caption tetap rapi sedangkan suara tetap natural.
* Setelah mengubah teks di sini, jalankan ulang:  ./render_preview.sh  atau  ./render_final.sh
  (audio yang teksnya tidak berubah diambil dari cache, jadi cepat).
"""

import re

VOICE = "id-ID-ArdiNeural"  # alternatif: "id-ID-GadisNeural"
RATE = "+0%"
PITCH = "+0Hz"
SENTENCE_GAP = 0.28  # jeda (detik) antar kalimat di dalam satu segment

SCENES = [
    # ------------------------------------------------------------------ 1
    {
        "scene": "S01Intro",
        "title": "Pembukaan, Learning Outcomes, dan Outline",
        "segments": [
            ("s01_title",
             "Halo semuanya, selamat datang di Session 15. "
             "Hari ini kita akan membahas salah satu teknik desain algoritma yang paling sering muncul, "
             "baik di perkuliahan, di technical interview, maupun di competitive programming, yaitu Dynamic Programming. "
             "Studi kasus utama kita adalah Maximum Subarray Sum."),
            ("s01_lo2",
             "Ada dua learning outcome yang ingin kita capai. "
             "Pertama, LO 2: kalian mampu mengidentifikasi optimal substructure dan overlapping subproblems sebagai syarat penerapan DP. "
             "Kalian juga bisa membedakan DP dari greedy dan divide and conquer, "
             "serta menjelaskan kenapa algoritma Kadane termasuk DP."),
            ("s01_lo3",
             "Kedua, LO 3: kalian mampu mendesain algoritma Kadane dengan recurrence dp[i] = max(A[i], dp[i-1] + A[i]). "
             "Caranya dengan menerapkan empat langkah desain DP, yaitu characterize, define, compute, dan construct, "
             "lalu mengimplementasikannya dengan memoization maupun tabulation."),
            ("s01_outline",
             "Alurnya begini. Kita mulai dari paradigma DP, yaitu optimal substructure dan overlapping subproblems. "
             "Lalu kita bandingkan memoization dengan tabulation. "
             "Setelah itu kita masuk ke Maximum Subarray Sum dengan algoritma Kadane. "
             "Dan terakhir, kita diskusikan kenapa Kadane itu DP, dan bukan greedy."),
        ],
    },
    # ------------------------------------------------------------------ 2
    {
        "scene": "S02WhyDP",
        "title": "Why DP? Recursion Tree Fibonacci",
        "segments": [
            ("s02_code",
             "Kita mulai dengan satu latihan sederhana. Coba hitung fib(5) secara rekursif. "
             "Ini pseudocode-nya. Kalau n kurang dari atau sama dengan 1, kembalikan n. "
             "Kalau tidak, kembalikan FIB(n-1) + FIB(n-2)."),
            ("s02_tree",
             "Sekarang kita gambar recursion tree-nya. "
             "fib(5) memanggil fib(4) dan fib(3). "
             "fib(4) memanggil fib(3) dan fib(2), dan seterusnya, "
             "sampai semua cabang berhenti di base case, yaitu fib(1) dan fib(0)."),
            ("s02_question",
             "Pertanyaannya, berapa kali kita menghitung fib(2)? "
             "Perhatikan lingkaran merah. Ternyata fib(2) dihitung sebanyak tiga kali. "
             "Bagaimana dengan fib(3)? Lingkaran biru menunjukkan fib(3) dihitung dua kali."),
            ("s02_problem",
             "Inilah sumber masalahnya. Subproblem yang sama muncul lagi dan lagi. "
             "Semakin besar n, pengulangan ini meledak secara eksponensial, sehingga kompleksitasnya menjadi O(2^n). "
             "Nah, bagaimana kalau hasilnya kita catat pada saat pertama kali dihitung?"),
        ],
    },
    # ------------------------------------------------------------------ 3
    {
        "scene": "S03Memoization",
        "title": "Memoization pada Fibonacci",
        "segments": [
            ("s03_code1",
             "Itulah ide dari memoization. Perhatikan pseudocode MEMOIZED-FIB. "
             "Kita siapkan sebuah array memo dari 0 sampai n, lalu semua isinya kita set NIL, "
             "yang artinya belum pernah dihitung."),
            ("s03_code2",
             "Di fungsi MEMOIZED-FIB-AUX, setelah base case, kita cek dulu. "
             "Kalau memo[n] tidak NIL, berarti nilainya sudah tersimpan, jadi langsung kembalikan saja, tidak perlu dihitung ulang. "
             "Kalau belum, kita hitung secara rekursif, simpan hasilnya ke memo[n], baru kemudian dikembalikan."),
            ("s03_trace",
             "Mari kita lihat efeknya. Pemanggilan pertama turun di sepanjang cabang kiri, "
             "dari fib(5), fib(4), fib(3), fib(2), sampai fib(1) dan fib(0). "
             "Setiap kali sebuah nilai selesai dihitung, nilai itu langsung disimpan ke dalam array memo."),
            ("s03_hit",
             "Ketika fib(4) membutuhkan fib(2), dan fib(5) membutuhkan fib(3), nilainya sudah ada di memo. "
             "Jadi subproblem yang sama memang tetap dipanggil, tetapi tidak dihitung lebih jauh. "
             "Recursion tree-nya menyusut drastis."),
            ("s03_complexity",
             "Karena setiap subproblem diselesaikan paling banyak satu kali, "
             "kompleksitas waktunya turun dari O(2^n) menjadi O(n)."),
        ],
    },
    # ------------------------------------------------------------------ 4
    {
        "scene": "S04Definition",
        "title": "Definisi Dynamic Programming",
        "segments": [
            ("s04_def",
             "Sekarang kita formalkan. Dynamic Programming adalah teknik desain algoritma "
             "untuk menyelesaikan masalah yang memiliki overlapping subproblems dan optimal substructure, "
             "dengan cara menyimpan hasil antara."),
            ("s04_props",
             "Jadi, DP bisa diterapkan kalau dua syarat terpenuhi. "
             "Pertama, optimal substructure: solusi optimal dari sebuah masalah mengandung solusi optimal dari subproblem-subproblem-nya. "
             "Kedua, overlapping subproblems: subproblem yang sama diselesaikan berulang kali dalam solusi rekursif yang naif, "
             "persis seperti fib(2) dan fib(3) tadi."),
            ("s04_contrast",
             "Ini berbeda dengan Divide and Conquer, yang subproblem-nya saling independen dan tidak tumpang tindih. "
             "DP juga berbeda dengan Greedy. Greedy memang memiliki optimal substructure, "
             "tetapi hanya mengambil satu pilihan greedy di setiap langkah, tanpa mengevaluasi ulang."),
        ],
    },
    # ------------------------------------------------------------------ 5
    {
        "scene": "S05TopDownBottomUp",
        "title": "Top-down (Memoization) vs Bottom-up (Tabulation)",
        "segments": [
            ("s05_two",
             "Ada dua cara mengimplementasikan DP. "
             "Yang pertama top-down, atau memoization: kita tulis rekursi yang natural, lalu cache hasilnya supaya tidak dihitung ulang. "
             "Yang kedua bottom-up, atau tabulation: kita isi sebuah tabel dengan urutan yang menjamin "
             "setiap subproblem sudah diselesaikan sebelum dibutuhkan."),
            ("s05_question",
             "MEMOIZED-FIB yang tadi adalah contoh implementasi top-down. "
             "Pertanyaannya, bisakah kita mengubahnya menjadi bottom-up?"),
            ("s05_code",
             "Tentu bisa. Ini FIB-DP. Kita buat array dp dari 0 sampai n, "
             "lalu isi dp[0] = 0 dan dp[1] = 1. "
             "Kemudian untuk i dari 2 sampai n, dp[i] = dp[i-1] + dp[i-2]. "
             "Terakhir, kembalikan dp[n]."),
            ("s05_fill",
             "Perhatikan arah pengisiannya, dari kiri ke kanan. "
             "dp[2] = 1, dp[3] = 2, dp[4] = 3, dan dp[5] = 5. "
             "Tidak ada rekursi sama sekali. Cukup satu loop, sehingga kompleksitas waktunya juga O(n)."),
            ("s05_table",
             "Lalu apa bedanya? Dari sisi komputasi, memoization hanya menghitung subproblem yang benar-benar dibutuhkan, "
             "sedangkan tabulation menghitung semua subproblem. "
             "Dari sisi space, memoization butuh space sebesar jumlah subproblem yang dihitung, sedangkan tabulation sebesar ukuran tabel. "
             "Dan dari sisi overhead, memoization terbebani oleh rekursi, sementara tabulation cukup dengan iterasi."),
        ],
    },
    # ------------------------------------------------------------------ 6
    {
        "scene": "S06DesignSteps",
        "title": "Empat Langkah Desain DP",
        "segments": [
            ("s06_steps",
             "Secara umum, ada empat langkah untuk mendesain algoritma DP. "
             "Satu, characterize: pahami struktur dari solusi optimal. "
             "Dua, define: definisikan nilai solusi optimal secara rekursif. "
             "Tiga, compute: hitung nilainya secara bottom-up, atau top-down dengan memoization. "
             "Empat, construct: bangun solusi optimalnya dari informasi yang sudah dihitung."),
            ("s06_apply",
             "Keempat langkah ini akan kita pakai satu per satu untuk menyelesaikan masalah utama kita hari ini."),
        ],
    },
    # ------------------------------------------------------------------ 7
    {
        "scene": "S07Problem",
        "title": "Maximum Subarray Sum: Problem",
        "segments": [
            ("s07_statement",
             "Masalahnya begini. Diberikan sebuah array A dari 1 sampai n berisi bilangan bulat, yang bisa saja negatif. "
             "Cari subarray yang contiguous, artinya elemennya berurutan tanpa melompat, "
             "yaitu A[i..j], yang jumlahnya paling besar."),
            ("s07_example",
             "Contohnya array ini: -2, 1, -3, 4, -1, 2, 1, -5, 4. "
             "Jawabannya adalah A[4..7], yaitu 4, -1, 2, 1, dengan jumlah 6."),
            ("s07_insight",
             "Perhatikan, subarray terbaik ini justru mengandung -1. "
             "Jadi kita tidak bisa sekadar mengambil angka positif saja. "
             "Kadang, menelan angka negatif itu menguntungkan, asalkan setelahnya ada angka positif yang lebih besar."),
        ],
    },
    # ------------------------------------------------------------------ 8
    {
        "scene": "S08Naive",
        "title": "Naive Approach dan Overlapping Subproblems",
        "segments": [
            ("s08_enum",
             "Pendekatan paling naif adalah mencoba semua kemungkinan. "
             "Untuk setiap index i, ada tepat i subarray yang berakhir di index tersebut. "
             "Di index 1 hanya ada satu, di index 2 ada dua, di index 3 ada tiga, dan seterusnya sampai index n."),
            ("s08_count",
             "Jadi total ada 1 + 2 + 3 + ... + n, atau O(n²) subarray. "
             "Untuk setiap subarray, menghitung jumlahnya butuh O(n). "
             "Total kompleksitasnya menjadi O(n³)."),
            ("s08_code",
             "Ini pseudocode BRUTE-FORCE-SUM. Loop pertama memilih end index, "
             "loop kedua mencari setiap kemungkinan start index, "
             "dan loop ketiga menjumlahkan elemen dari start sampai end. "
             "Setiap hasilnya dibandingkan dengan global_max. Tiga loop bersarang, itulah sumber O(n³)."),
            ("s08_overlap",
             "Sekarang perhatikan baik-baik. Saat i = 2, kita menjumlahkan A[1] dan A[2]. "
             "Saat i = 3, kita kembali menjumlahkan A[1] dan A[2], baru kemudian menambahkan A[3]. "
             "Bagian yang sama dihitung berulang kali. Overlapping subproblems terjadi di mana-mana."),
            ("s08_idea",
             "Kalau dilihat lebih dekat, sebenarnya kita hanya peduli pada jumlah maksimum yang berakhir di index sebelumnya. "
             "Jadi, bagaimana kalau kita simpan jumlah maksimum untuk setiap ending index?"),
        ],
    },
    # ------------------------------------------------------------------ 9
    {
        "scene": "S09Characterize",
        "title": "Step 1 & Step 2: Characterize dan Define",
        "segments": [
            ("s09_def",
             "Inilah langkah pertama, characterize. Kita definisikan subproblem-nya: "
             "dp[i] adalah jumlah subarray maksimum yang berakhir tepat di index i."),
            ("s09_options",
             "Subarray optimal yang berakhir di index i hanya punya dua pilihan struktural. "
             "Opsi A, extend: lanjutkan subarray optimal yang berakhir di i-1, lalu tambahkan A[i]. "
             "Opsi B, start: mulai subarray yang benar-benar baru di index i, kalau opsi A memberikan nilai yang lebih kecil."),
            ("s09_theorem",
             "Dari sini kita mendapatkan teoremanya: solusi optimal untuk subproblem di index i "
             "mengandung solusi optimal untuk subproblem di index i-1. Itulah optimal substructure."),
            ("s09_recurrence",
             "Langkah kedua, define. Dua opsi tadi langsung kita tulis sebagai recurrence: "
             "dp[i] = max(A[i], dp[i-1] + A[i]). "
             "Suku pertama adalah opsi start, suku kedua adalah opsi extend."),
            ("s09_base",
             "Base case-nya, kita tidak bisa melihat ke belakang sebelum elemen pertama, jadi dp[1] = A[1]. "
             "Dan karena subarray maksimum bisa berakhir di mana saja, "
             "jawaban akhirnya adalah GlobalMax, yaitu nilai maksimum dari semua dp[i], untuk i dari 1 sampai n."),
        ],
    },
    # ------------------------------------------------------------------ 10
    {
        "scene": "S10Compute",
        "title": "Step 3: Compute Bottom-up",
        "segments": [
            ("s10_code",
             "Langkah ketiga, compute. Ini KADANE-TABLE. "
             "Kita isi dp[1] dengan A[1], dan global_max juga A[1]. "
             "Lalu untuk i dari 2 sampai n, hitung dp[i] dengan recurrence tadi, "
             "dan perbarui global_max kalau dp[i] lebih besar."),
            ("s10_fill1",
             "Mari kita jalankan pada contoh kita. dp[1] = -2. "
             "dp[2] = max(1, -2 + 1) = 1, artinya kita mulai baru. "
             "dp[3] = max(-3, 1 + (-3)) = -2, artinya kita extend."),
            ("s10_fill2",
             "dp[4] = max(4, -2 + 4) = 4, mulai baru lagi. "
             "Lalu kita terus extend: dp[5] = 3, dp[6] = 5, dan dp[7] = 6. "
             "Kemudian dp[8] = 1, dan dp[9] = 5. "
             "Nilai maksimum di tabel adalah 6, sesuai dengan jawaban kita."),
            ("s10_observe",
             "Perhatikan, untuk menghitung dp[i], kita hanya pernah melihat dp[i-1]. "
             "Jadi seluruh array sebenarnya tidak perlu disimpan. Cukup satu variabel untuk melacak state."),
            ("s10_space",
             "Hasilnya adalah KADANE-SPACE-OPTIMIZED. Array dp diganti dengan satu variabel, curr_max. "
             "Dengan begitu, space complexity turun dari O(n) menjadi O(1), sementara waktunya tetap O(n). "
             "Pelajaran pentingnya: algoritma DP tidak selalu tentang tabel."),
            ("s10_fib",
             "Sebenarnya, kalian mungkin sudah pernah melakukan trik ini di Fibonacci. "
             "FIB-SPACE-OPTIMIZED hanya menyimpan dua nilai terakhir, prev1 dan prev2, "
             "lalu menggesernya di setiap iterasi."),
        ],
    },
    # ------------------------------------------------------------------ 11
    {
        "scene": "S11Construct",
        "title": "Step 4: Construct the Solution",
        "segments": [
            ("s11_question",
             "Sekarang kita sudah punya nilai optimalnya. Tapi bagaimana kalau kita ingin tahu, "
             "subarray mana yang menghasilkan nilai itu? "
             "Untuk itu kita butuh informasi index. Jadi, kita lacak batas index setiap kali nilainya berubah."),
            ("s11_rules",
             "Ada dua aturan. Expansion rule: kalau curr_max di-reset, batas awal bergeser ke index saat ini. "
             "Global rule: kalau tercapai global maximum yang baru, simpan batas start dan end secara permanen."),
            ("s11_code",
             "Ini KADANE-CONSTRUCT. Kita tambahkan tiga variabel: start, end, dan temp_start. "
             "Saat A[i] lebih besar dari curr_max + A[i], kita reset, dan temp_start menjadi i. "
             "Saat curr_max melampaui global_max, start diisi dengan temp_start, dan end diisi dengan i."),
            ("s11_init",
             "Mari kita trace pada array -2, 1, -3, 4, -1, 2, 1. "
             "Inisialisasi: curr_max dan global_max sama-sama -2, dan subarray-nya hanya -2."),
            ("s11_i23",
             "i = 2: max(1, -2 + 1) = 1. Ini reset, temp_start pindah ke 2, dan global_max naik menjadi 1. "
             "i = 3: max(-3, 1 + (-3)) = -2. Kita extend, tapi global_max tetap 1."),
            ("s11_i45",
             "i = 4: max(4, -2 + 4) = 4. Reset lagi, temp_start pindah ke 4, dan global_max naik menjadi 4. "
             "i = 5: curr_max menjadi 3, sedangkan global_max tetap 4."),
            ("s11_i67",
             "i = 6: curr_max menjadi 5, dan global_max ikut naik. "
             "Terakhir i = 7: curr_max menjadi 6, dan global_max naik menjadi 6. "
             "Jadi start = 4, end = 7, dan subarray-nya adalah 4, -1, 2, 1, dengan jumlah 6."),
        ],
    },
    # ------------------------------------------------------------------ 12
    {
        "scene": "S12WhyNotGreedy",
        "title": "Why Kadane's is DP and Not Greedy",
        "segments": [
            ("s12_props",
             "Sekarang pertanyaan terakhir: kenapa Kadane itu DP, dan bukan greedy? "
             "Pertama, Kadane memenuhi kedua properti DP. "
             "Optimal substructure: subarray optimal yang berakhir di i adalah A[i] sendirian, "
             "atau A[i] yang ditempelkan ke subarray optimal yang berakhir di i-1. "
             "Solusi subproblem-nya dipakai secara langsung."),
            ("s12_overlap",
             "Overlapping subproblems: kalau untuk setiap i kita bertanya, berapa subarray terbaik yang berakhir di i, "
             "lalu menghitungnya dari nol setiap kali, kita akan memeriksa prefix yang sama berulang-ulang. "
             "DP menghindari hal itu dengan dp[i-1], atau curr_max."),
            ("s12_greedy",
             "Algoritma greedy akan melakukan satu kali pass dengan aturan yang tetap. "
             "Misalnya aturannya: ambil elemen selama positif, dan reset ketika bertemu angka negatif. "
             "Coba kita jalankan pada A = -1, 3, -1, 4."),
            ("s12_fail",
             "Greedy mengambil 3, lalu bertemu -1 di index 3 dan langsung reset. "
             "Setelah itu ia mengambil 4. Hasil terbaiknya hanya 4. "
             "Padahal subarray 3, -1, 4 memberikan jumlah 6. Greedy melewatkannya."),
            ("s12_kadane",
             "Kadane berbeda. Di index 3, curr_max = 3 + (-1) = 2, masih lebih baik daripada mulai baru dari -1, jadi ia extend. "
             "Di index 4, 2 + 4 = 6. "
             "Kadane membuat keputusan di setiap langkah, extend atau restart, berdasarkan state yang sudah dihitung sebelumnya, yaitu dp[i-1]. "
             "Itu adalah keputusan DP, bukan pilihan greedy."),
            ("s12_table",
             "Ringkasnya begini. Greedy memutuskan hanya dari input mentah atau heuristik di langkah saat ini, "
             "sedangkan DP memakai state subproblem yang sudah dihitung. "
             "Greedy memilih sebelum menyelesaikan subproblem, sementara DP memilih setelah mengevaluasi subproblem sebelumnya. "
             "Greedy tidak pernah melihat ke belakang, sedangkan DP justru harus membaca tabel atau state yang sudah diselesaikan."),
            ("s12_examples",
             "Contoh algoritma greedy adalah Activity Selection, Fractional Knapsack, Huffman Code, dan Dijkstra. "
             "Sedangkan contoh DP adalah Max Subarray Sum, 0/1 Knapsack, dan Coin Change untuk sistem koin yang non-canonical."),
        ],
    },
    # ------------------------------------------------------------------ 13
    {
        "scene": "S13Summary",
        "title": "Summary",
        "segments": [
            ("s13_a",
             "Mari kita rangkum. Satu, DP menyelesaikan masalah dengan meng-cache solusi dari overlapping subproblems, "
             "dan membutuhkan optimal substructure. "
             "Dua, memoization bersifat top-down, yaitu meng-cache pemanggilan rekursif, "
             "sedangkan tabulation bersifat bottom-up, yaitu mengisi tabel secara iteratif."),
            ("s13_b",
             "Tiga, algoritma Kadane: dp[i] = max(A[i], dp[i-1] + A[i]), dengan waktu O(n), "
             "dan space O(1) pada versi yang dioptimasi. "
             "Empat, Kadane adalah DP karena setiap dp[i] bergantung pada dp[i-1], "
             "dan keputusannya tidak bisa dibuat secara greedy tanpa mengetahui state optimal sebelumnya."),
        ],
    },
    # ------------------------------------------------------------------ 14
    {
        "scene": "S14Exercise",
        "title": "Exercise dan References",
        "segments": [
            ("s14_stairs",
             "Sebelum kita tutup, ada dua latihan untuk kalian. "
             "Latihan pertama, Climbing Stairs. Ada sebuah tangga dengan n anak tangga. "
             "Setiap kali melangkah, kalian boleh naik 1 atau 2 anak tangga. "
             "Berapa banyak cara berbeda untuk sampai ke puncak? "
             "Contohnya, untuk n = 3 jawabannya 3, yaitu 1+1+1, 1+2, atau 2+1."),
            ("s14_stairs_task",
             "Tugas kalian: tuliskan pseudocode-nya dengan pendekatan DP menggunakan empat langkah tadi. "
             "Petunjuknya, pikirkan dari anak tangga mana saja kalian bisa sampai ke anak tangga terakhir. "
             "Mungkin polanya akan terasa familiar."),
            ("s14_product",
             "Latihan kedua, Maximum Product Subarray. Cari subarray contiguous yang hasil kalinya paling besar. "
             "Contohnya, untuk A = -1, 3, -4, -2, jawabannya 24, dari subarray 3, -4, -2."),
            ("s14_product_task",
             "Pertanyaannya, kenapa algoritma Kadane yang standar tidak berhasil di sini? "
             "Bagaimana cara membuatnya berhasil, dan kenapa? "
             "Petunjuknya, perhatikan apa yang terjadi ketika bilangan negatif dikalikan dengan bilangan negatif."),
            ("s14_refs",
             "Referensi untuk sesi ini adalah Cormen dan kawan-kawan, Introduction to Algorithms edisi keempat, bab 14.3, "
             "dan Skiena, The Algorithm Design Manual edisi ketiga, bab 10.1. "
             "Terima kasih, dan sampai jumpa di sesi berikutnya!"),
        ],
    },
]


# --------------------------------------------------------------------------
# Konversi teks caption -> teks ucapan (khusus TTS). Caption tidak berubah.
# --------------------------------------------------------------------------
_SPEECH_RULES = [
    (r"O\(2\^n\)", "big O dua pangkat n"),
    (r"O\(n²\)", "big O n kuadrat"),
    (r"O\(n³\)", "big O n pangkat tiga"),
    (r"O\(n\)", "big O n"),
    (r"O\(1\)", "big O satu"),
    (r"\+\s*\.\.\.\s*\+", " sampai "),
    (r"\.\.\.", " sampai "),
    (r"A\[(\w+)\.\.(\w+)\]", r"A \1 sampai \2"),
    (r"(dp|A|memo|FIB|fib)\[([^\]]+)\]", r"\1 \2"),
    (r"(FIB|fib)\(([^)]+)\)", r"fib \2"),
    (r"\bdp\b", "d p"),
    (r"\bLO (\d)", r"L O \1"),
    (r"0/1 Knapsack", "zero one Knapsack"),
    (r"MEMOIZED-FIB-AUX", "memoized fib aux"),
    (r"MEMOIZED-FIB", "memoized fib"),
    (r"FIB-SPACE-OPTIMIZED", "fib space optimized"),
    (r"FIB-DP", "fib d p"),
    (r"KADANE-SPACE-OPTIMIZED", "Kadane space optimized"),
    (r"KADANE-TABLE", "Kadane table"),
    (r"KADANE-CONSTRUCT", "Kadane construct"),
    (r"BRUTE-FORCE-SUM", "brute force sum"),
    (r"_", " "),
    (r"\(-(\d)\)", r"minus \1"),
    (r"max\(([^,()]+),\s*([^()]+)\)(\s*=\s*)?",
     lambda m: f"max dari {m.group(1)} dan {m.group(2)}" + (", hasilnya " if m.group(3) else "")),
    (r"(?<![\w)])-(\d)", r"minus \1"),
    (r"(\w)\s*-\s*(\d)", r"\1 minus \2"),
    (r"\s*\+\s*", " plus "),
    (r"\s=\s", " sama dengan "),
    (r"[()]", " "),
    (r"\s{2,}", " "),
]


def to_speech(text: str) -> str:
    out = text
    for pat, rep in _SPEECH_RULES:
        out = re.sub(pat, rep, out)
    return out.strip()


def split_sentences(text: str):
    """Pisahkan segment menjadi kalimat (satu kalimat = satu file TTS = satu cue caption utama)."""
    parts = re.split(r"(?<=[.!?])(?<!\.\.\.)\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def all_segments():
    for sc in SCENES:
        for seg_id, text in sc["segments"]:
            yield sc["scene"], seg_id, text
