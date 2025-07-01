1
2 # include < HX711 .h >
3 # include < ESP32Servo .h >
4 # include < SPI .h >
5 # include < MFRC522 .h >
6 # include < WiFi .h >
7 # include < Firebase_ESP_Client .h >
8
9 // Firebase helper files
10 # include " addons / TokenHelper .h"
11 # include " addons / RTDBHelper .h"
12
13 // WiFi and Firebase configuration ( replace with your credentials )
14 # define WIFI_SSID ""
15 # define WIFI_PASSWORD ""
16 # define API_KEY ""
17 # define DATABASE_URL ""
18 # define USER_EMAIL ""
19 # define USER_PASSWORD ""
20
21 // Pin definitions
22 # define LOADCELL_DT
23 # define LOADCELL_SCK
24 # define SERVO_PIN
25 # define RED_LED
26 # define GREEN_LED
27 # define BUTTON_PIN
28 # define VIBRATION_PIN
29
30 # define SS_PIN
31 # define RST_PIN
32 # define SCK_PIN
33 # define MOSI_PIN
34 # define MISO_PIN
35
36 // Global objects and flags
37 HX711 scale ;
38 Servo lockServo ;
39 MFRC522 rfid ( SS_PIN , RST_PIN );
40 FirebaseData fbdo ;
41 FirebaseAuth auth ;
42 FirebaseConfig config ;
43
44 bool locked = false ;
45 bool lastVibrationState = false ;
46 bool weightAlert = false ;
47 bool firebaseConnected = false ;
48 bool bypassDone = false ;
49
50 unsigned long unlockUntil = 0;
51 unsigned long remoteUnlockUntil = 0;
52 unsigned long lastVibrationTime = 0;
53 const unsigned long unlockDuration = 5000;
54 const unsigned long remoteUnlockDuration = 5000;
55 const float weightThreshold = 0.01;
56
57 // Authorized RFID cards ( example UIDs )
58 byte authorizedUIDs [][4] = {
59
60 };
61 const int authorizedCount = sizeof ( authorizedUIDs ) / sizeof (
authorizedUIDs [0]) ;
62
63 // Function : Check if scanned UID matches any authorized UID
64 bool isAuthorized ( byte * scannedUID ) {
65 for ( int i = 0; i < authorizedCount ; i ++) {
66 bool match = true ;
67 for ( int j = 0; j < 4; j ++) {
68 if ( scannedUID [j] != authorizedUIDs [i ][ j ]) {
69 match = false ;
70 break ;
71 }
72 }
73 if ( match ) return true ;
74 }
75 return false ;
76 }
77
78 // Function : Update servo and LED based on lock state
79 void updateLockState () {
80 if ( locked ) {
81 lockServo . write (0) ;
82 digitalWrite ( RED_LED , HIGH );
83 digitalWrite ( GREEN_LED , LOW );
84 } else {
85 lockServo . write (90) ;
86 digitalWrite ( RED_LED , LOW );
87 digitalWrite ( GREEN_LED , HIGH ) ;
88 }
89 }
90
91 // Function : Perform hard reset on RFID module
92 void resetRFID () {
93 digitalWrite ( RST_PIN , LOW );
94 delay (100) ;
95 digitalWrite ( RST_PIN , HIGH );
96 delay (500) ;
97 rfid . PCD_Init () ;
98 rfid . PCD_SetAntennaGain ( MFRC522 :: RxGain_max );
99 }
100
101 // Function : Setup Firebase connection
102 bool setupFirebase () {
103 config . database_url = DATABASE_URL ;
104 config . api_key = API_KEY ;
105 config . time_zone = 3;
106 auth . user . email = USER_EMAIL ;
107 auth . user . password = USER_PASSWORD ;
108
109 Firebase . signUp (& config , & auth , USER_EMAIL , USER_PASSWORD );
110 Firebase . begin (& config , & auth );
111 Firebase . reconnectWiFi ( true );
112
113 unsigned long startTime = millis () ;
114 while (! Firebase . ready () && millis () - startTime < 10000) {
115 delay (300) ;
116 }
117 return Firebase . ready () ;
118 }
119
120 // Function : Check for RFID card and handle authentication
121 void checkRFID () {
122 if (! rfid . PICC_IsNewCardPresent () ) return ;
123
124 if (! rfid . PICC_ReadCardSerial () ) {
125 Serial . println (" Failed to read UID. Resetting RFID ... ");
126 resetRFID () ;
127 return ;
128 }
129
130 Serial . print (" UID read : ");
131 for ( byte i = 0; i < rfid . uid . size ; i ++) {
132 Serial . print ( rfid . uid . uidByte [ i] < 0 x10 ? "0" : "");
133 Serial . print ( rfid . uid . uidByte [ i], HEX );
134 Serial . print (" ");
135 }
136 Serial . println () ;
137
138 if ( isAuthorized ( rfid . uid . uidByte ) ) {
139 Serial . println (" Authorized card . Unlocking ...");
140 locked = false ;
141 updateLockState () ;
142 remoteUnlockUntil = millis () + unlockDuration ;
143 bypassDone = false ;
144
145 if ( firebaseConnected ) {
146 Firebase . RTDB . setBool (& fbdo , "/ guardbox / locked ",
false );
147 Firebase . RTDB . setString (& fbdo , "/ guardbox / event ",
" RFID unlocked ");
148 }
149 } else {
150 Serial . println (" Unauthorized card .") ;
151 if ( firebaseConnected ) {
152 Firebase . RTDB . setString (& fbdo , "/ guardbox / event ",
" Unauthorized RFID attempt ");
153 }
154 }
155
156 rfid . PICC_HaltA () ;
157 rfid . PCD_StopCrypto1 () ;
158 }
159
160 // Function : Initial setup
161 void setup () {
162 Serial . begin (115200) ;
163 pinMode ( RED_LED , OUTPUT );
164 pinMode ( GREEN_LED , OUTPUT );
165 pinMode ( BUTTON_PIN , INPUT_PULLUP );
166 pinMode ( VIBRATION_PIN , INPUT ) ;
167 pinMode ( RST_PIN , OUTPUT );
168 digitalWrite ( RST_PIN , HIGH );
169
170 lockServo . attach ( SERVO_PIN );
171 updateLockState () ;
172 delay (1000) ;
173
174 Serial . println (" GuardBox starting ... ");
175
176 // Initialize weight sensor
177 scale . begin ( LOADCELL_DT , LOADCELL_SCK );
178 scale . set_scale (1500) ;
179 scale . tare () ;
180
181 // Initialize SPI and RFID
182 SPI . begin ( SCK_PIN , MISO_PIN , MOSI_PIN , SS_PIN );
183 resetRFID () ;
184
185 // WiFi setup
186 WiFi . begin ( WIFI_SSID , WIFI_PASSWORD );
187 Serial . print (" Connecting to WiFi ");
188 unsigned long startTime = millis () ;
189 while ( WiFi . status () != WL_CONNECTED && millis () - startTime <
20000) {
190 Serial . print (".");
191 delay (500) ;
192 }
193 Serial . println () ;
194
195 if ( WiFi . status () == WL_CONNECTED ) {
196 Serial . println (" WiFi connected .");
197 firebaseConnected = setupFirebase () ;
198 if ( firebaseConnected ) Serial . println (" Firebase connected
.") ;
199 }
200
201 updateLockState () ;
202 Serial . println (" GuardBox is ready .") ;
203 }
204
205 // Function : Main control loop
206 void loop () {
207 checkRFID () ;
208
209 // Print debug info every 5 seconds
210 static unsigned long lastDebugTime = 0;
211 if ( millis () - lastDebugTime > 5000) {
212 float weight = abs ( scale . get_units (3) );
213 bool doorClosed = digitalRead ( BUTTON_PIN ) == LOW ;
214 Serial . printf (" Door : %s | Weight : %.2 f | Locked : %s\n",
215 doorClosed ? " Closed " : " Open ",
216 weight ,
217 locked ? " Yes " : "No"
218 );
219 lastDebugTime = millis () ;
220 }
221
222 // Handle bypass ( unlock delay )
223 if ( millis () < remoteUnlockUntil ) {
224 if ( locked && ! bypassDone ) {
225 locked = false ;
226 updateLockState () ;
227 bypassDone = true ;
228 if ( firebaseConnected ) {
229 Firebase . RTDB . setBool (& fbdo , "/ guardbox /
locked ", false );
230 }
231 }
232 delay (50) ;
233 return ;
234 } else if ( bypassDone ) {
235 bypassDone = false ;
236 }
237
238 // Firebase lock control
239 if ( firebaseConnected && Firebase . ready () ) {
240 if ( Firebase . RTDB . getBool (& fbdo , "/ guardbox / locked ")) {
241 bool cloudLock = fbdo . boolData () ;
242 if ( cloudLock != locked ) {
243 locked = cloudLock ;
244 updateLockState () ;
245 if (! cloudLock ) remoteUnlockUntil =
millis () + remoteUnlockDuration ;
246 }
247 }
248 }
249
250 // WiFi reconnect logic
251 if ( WiFi . status () != WL_CONNECTED ) {
252 static unsigned long lastReconnectAttempt = 0;
253 if ( millis () - lastReconnectAttempt > 30000) {
254 WiFi . reconnect () ;
255 lastReconnectAttempt = millis () ;
256 delay (5000) ;
257 if ( WiFi . status () == WL_CONNECTED && !
firebaseConnected ) {
258 firebaseConnected = setupFirebase () ;
259 }
260 }
261 }
262
263 // Read sensors
264 float weight = abs ( scale . get_units (3) );
265 bool doorClosed = digitalRead ( BUTTON_PIN ) == LOW ;
266 bool vibration = digitalRead ( VIBRATION_PIN ) == HIGH ;
267
268 // Upload weight
269 if ( firebaseConnected && Firebase . ready () ) {
270 Firebase . RTDB . setFloat (& fbdo , "/ guardbox / weight ", weight )
;
271 }
272
273 // Auto - lock after placing a package
274 if (! locked && doorClosed && weight >= weightThreshold && millis
() >= remoteUnlockUntil ) {
275 locked = true ;
276 updateLockState () ;
277 if ( firebaseConnected ) {
278 Firebase . RTDB . setBool (& fbdo , "/ guardbox / locked ",
true );
279 Firebase . RTDB . setString (& fbdo , "/ guardbox / event ",
" Box locked due to weight ");
280 }
281 }
282
283 // Notify if empty and unlocked
284 static unsigned long lastEmptyNotification = 0;
285 if (! locked && doorClosed && weight < weightThreshold && millis ()
- lastEmptyNotification > 60000) {
286 if ( firebaseConnected ) {
287 Firebase . RTDB . setString (& fbdo , "/ guardbox / event ",
" Box empty - not locked ") ;
288 }
289 lastEmptyNotification = millis () ;
290 }
291
292 // Auto - unlock if door opened
293 if ( locked && ! doorClosed ) {
294 locked = false ;
295 updateLockState () ;
296 if ( firebaseConnected ) {
297 Firebase . RTDB . setBool (& fbdo , "/ guardbox / locked ",
false );
298 Firebase . RTDB . setString (& fbdo , "/ guardbox / event ",
" Box unlocked due to door open ");
299 }
300 }
301
302 // Vibration detection
303 if ( vibration && ! lastVibrationState ) {
304 if ( firebaseConnected ) {
305 Firebase . RTDB . setString (& fbdo , "/ guardbox / event ",
" Vibration detected ");
306 }
307 digitalWrite ( RED_LED , HIGH );
308 digitalWrite ( GREEN_LED , LOW );
309 lastVibrationTime = millis () ;
310 }
311
312 lastVibrationState = vibration ;
313
314 // Weight dropped alert
315 if ( weight < weightThreshold && ! weightAlert ) {
316 weightAlert = true ;
317 if ( firebaseConnected ) {
318 Firebase . RTDB . setString (& fbdo , "/ guardbox / event ",
" Weight dropped ");
319 }
320 } else if ( weight >= weightThreshold && weightAlert ) {
321 weightAlert = false ;
322 if ( firebaseConnected ) {
323 Firebase . RTDB . setString (& fbdo , "/ guardbox / event ",
" Weight normal ");
324 }
325 }
326
327 delay (50) ;
