# ui-ir

## Project setup
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn serve
```

### Compiles and minifies for production
```
yarn build
```

### Lints and fixes files
```
yarn lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

# Nguyễn Hữu Quyền - 18521321
Trong phần thu thập dữ liệu, để đạt được hiệu quả của mô hình thì bộ dữ liệu được thu thập cần được thu thập với một lượng vừa đủ, song để thu thập các gói tin mạng cũng như giả lập tấn công để thu thập dữ liệu đòi hỏi lượng kiến thức vững về lĩnh vực an ninh mạng.//
Nên ở đây em quyết định sử dụng bộ dữ liệu đã được nhóm nghiên cứu khác công bố và được công bố trên Network and Distributed System Security (NDSS) là Kitsune được lấy từ https://www.kaggle.com/ymirsky/network-attack-dataset-kitsune. //
Trong bộ dữ liệu này, toàn bộ các mẫu đã được thu thập từ tệp gói tin mạng dạng pcap và phân tích ra thành tệp csv. Bộ dữ liệu này gồm 9 bộ dữ liệu con và mỗi bộ dữ liệu con tương ứng với 1 loại tấn công: Mirai, Active Wiretap, Fuzzing, ARP MitM, OS Scan, SSDP Flood, SSL Renegotiation, SYN DoS và Video Injection. Dữ liệu này được phân bố như hình~\ref{fig:dis}. Và trong các bộ dữ liệu con này mỗi mẫu sẽ gồm có 115 đặc trưng (features) và sẽ được đánh một trong 2 nhãn (label) bao gồm 0 - benign và 1 - malicious. Dữ liệu trong Kitsune được thu thập bằng cách tự tấn công và phân tích các đặc trưng trong tập tin bị tấn công đó.//
Ở đây em chọn bộ Fuzzing vì loại tấn công này có số lượng bản ghi có nhãn normal (432.783 records) gần xấp xỉ 4.5 lần nhãn attack (1.811.356 records) hoàn toàn thích hợp cho việc cân bằng dữ liệu để cải tiến hiệu quả mô hình. Bộ Fuzzing sẽ được chia ra hai phần: một phần dùng để huấn luyện 80% và một phần để kiểm tra đánh giá 20%.
