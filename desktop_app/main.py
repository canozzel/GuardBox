1 from kivymd . app import MDApp
2 from kivymd . uix . boxlayout import MDBoxLayout
3 from kivymd . uix . label import MDLabel
4 from kivymd . uix . button import MDRaisedButton
5 from kivymd . uix . card import MDCard
6 from kivy . uix . image import Image
7 from kivy . uix . widget import Widget
8 from kivy . clock import Clock
9 from kivy . core . window import Window
10 from plyer import notification
11 from kivy . uix . scrollview import ScrollView
12 import threading
13 import pyrebase
14 import time
15
16 # Window size
17 Window . size = (1000 , 600)
18
19 # Firebase Config
20 firebase_config = {
21
22 }
23
24 firebase = pyrebase . initialize_app ( firebase_config )
25 db = firebase . database ()
26 WEIGHT_THRESHOLD = 1000 # threshold
27
28 class TopBar ( MDBoxLayout ):
29 def __init__ ( self , ** kwargs ):
30 super () . __init__ (** kwargs )
31 self . orientation = 'horizontal '
32 self . size_hint_y = None
33 self . height = "60 dp"
34 self . padding = [15 , 10]
35 self . md_bg_color = (0.05 , 0.05 , 0.1 , 1)
36
37 # Logo
38 self . logo = Image (
39 source =" logo . jpg ",
40 size_hint =( None , None ) ,
41 size =("40 dp", "40 dp") ,
42 allow_stretch = True
43 )
44 self . add_widget ( self . logo )
45
46 # App Title
47 self . title = MDLabel (
48 text =" GuardBox ",
49 font_style ="H6",
50 theme_text_color =" Custom ",
51 text_color =(1 , 1 , 1, 1) ,
52 halign =" left ",
53 valign =" middle ",
54 size_hint_x = None ,
55 width ="150 dp",
56 padding =(10 , 0)
57 )
58 self . add_widget ( self . title )
59
60 self . add_widget ( Widget () ) # Spacer
61
62 # Theme Toggle Button
63 self . theme_toggle = MDRaisedButton (
64 text =" Dark Mode ",
65 md_bg_color =(0.2 , 0.5 , 1 , 1) ,
66 size_hint =( None , None ) ,
67 size =(" 140 dp", "40 dp") ,
68 pos_hint ={" center_y ": 0.5} ,
69 on_release = self . toggle_theme
70 )
71 self . add_widget ( self . theme_toggle )
72
73 def toggle_theme ( self , * args ):
74 app = MDApp . get_running_app ()
75 if app . theme_cls . theme_style == " Dark ":
76 app . theme_cls . theme_style = " Light "
77 self . theme_toggle . text = " Light Mode "
78 else :
79 app . theme_cls . theme_style = " Dark "
80 self . theme_toggle . text = " Dark Mode "
81
82 class MainScreen ( MDBoxLayout ):
83 def __init__ ( self , ** kwargs ):
84 super () . __init__ (** kwargs )
85
86 self . orientation = " vertical "
87 self . spacing = 15
88 self . padding = [20 , 10]
89
90 # Top Bar
91 self . add_widget ( TopBar () )
92
93 # Middle Cards
94 cards = MDBoxLayout (
95 orientation =" horizontal ",
96 spacing =20 ,
97 size_hint_y = None ,
98 height =" 220 dp"
99 )
100
101 # Box Status Card
102 self . status_card = MDCard (
103 orientation =" vertical ",
104 padding =20 ,
105 radius =[15 , 15 , 15 , 15] ,
106 md_bg_color =(0.1 , 0.1 , 0.15 , 1) ,
107 size_hint =(0.5 , 1)
108 )
109
110 self . status_title = MDLabel (
111 text =" Box Status ",
112 halign =" center ",
113 font_style ="H4",
114 theme_text_color =" Custom ",
115 text_color =(0.5 , 0.7 , 1, 1) ,
116 size_hint_y = None ,
117 height =" 180 dp"
118 )
119
120 self . box_icon_and_text = MDBoxLayout (
121 orientation =" horizontal ",
122 spacing =10 ,
123 size_hint =( None , None ) ,
124 width ="180 dp",
125 height ="60 dp",
126 pos_hint ={" center_x ": 0.5}
127 )
128
129 self . box_image = Image (
130 source =" box . png ",
131 size_hint =( None , None ) ,
132 size =("40 dp", "40 dp") ,
133 size_hint_y = None ,
134 height =" 180 dp"
135 )
136
137 self . status_label = MDLabel (
138 text =" Empty ",
139 font_style ="H5",
140 theme_text_color =" Custom ",
141 text_color =(0.5 , 1, 0.5 , 1) ,
142 valign =" middle ",
143 size_hint =(1 , 1) ,
144 size_hint_y = None ,
145 height =" 180 dp"
146 )
147
148 self . box_icon_and_text . add_widget ( self . box_image )
149 self . box_icon_and_text . add_widget ( self . status_label )
150
151 self . status_card . add_widget ( self . status_title )
152 self . status_card . add_widget ( Widget ( size_hint_y = None , height ="10 dp") )
153 self . status_card . add_widget ( self . box_icon_and_text )
154
155 # Lock Control Card
156 self . lock_card = MDCard (
157 orientation =" vertical ",
158 padding =20 ,
159 radius =[15 , 15 , 15 , 15] ,
160 md_bg_color =(0.1 , 0.1 , 0.15 , 1) ,
161 size_hint =(0.5 , 1)
162 )
163 self . lock_title = MDLabel (
164 text =" Lock Control ",
165 halign =" center ",
166 font_style ="H4",
167 theme_text_color =" Custom ",
168 text_color =(0.5 , 0.7 , 1, 1) ,
169 size_hint_y = None ,
170 height ="60 dp",
171 size_hint_x = None ,
172 width = " 500 dp",
173 pos_hint = {" center_x ": 0.5 , " center_Y ": 0.5}
174 )
175
176 self . lock_icon_and_text = MDBoxLayout (
177 orientation =" horizontal ",
178 spacing =10 ,
179 size_hint =( None , None ) ,
180 width ="180 dp",
181 height ="60 dp",
182 pos_hint ={" center_x ": 0.5}
183 )
184
185 self . lock_image = Image (
186 source =" locked .png",
187 size_hint =( None , None ) ,
188 size =("40 dp", "40 dp") ,
189 size_hint_y = None ,
190 height ="60 dp"
191 )
192
193 self . lock_status = MDLabel (
194 text =" Locked ",
195 font_style ="H5",
196 theme_text_color =" Custom ",
197 text_color =(1 , 0.4 , 0.4 , 1) ,
198 valign =" middle ",
199 size_hint =(1 , 1)
200 )
201
202 self . lock_icon_and_text . add_widget ( self . lock_image )
203 self . lock_icon_and_text . add_widget ( self . lock_status )
204
205 self . btn_row = MDBoxLayout (
206 orientation =" horizontal ",
207 spacing =20 ,
208 size_hint =( None , None ) ,
209 size =(" 300 dp", "50 dp") ,
210 size_hint_x = None ,
211 width = "90 dp",
212 pos_hint = {" center_x ": 0.5 , " center_Y ": 0.5}
213 )
214
215 self . unlock_btn = MDRaisedButton (
216 text =" Unlock ",
217 font_size ="25",
218 md_bg_color =(0.2 , 0.8 , 0.2 , 1) ,
219 on_release = lambda x: self . send_command (" unlock ")
220 )
221
222 self . btn_row . add_widget ( self . unlock_btn )
223
224 self . lock_card . add_widget ( self . lock_title )
225 self . lock_card . add_widget ( Widget ( size_hint_y = None , height ="10 dp"))
226 self . lock_card . add_widget ( self . lock_icon_and_text )
227 self . lock_card . add_widget ( Widget ( size_hint_y = None , height ="10 dp"))
228 self . lock_card . add_widget ( self . btn_row )
229
230 cards . add_widget ( self . status_card )
231 cards . add_widget ( self . lock_card )
232 self . add_widget ( cards )
233
234 # Notification Section
235 self . notifications = []
236
237 self . notification_card = MDCard (
238 orientation =" vertical ",
239 padding =20 ,
240 radius =[15 , 15 , 15 , 15] ,
241 md_bg_color =(0.1 , 0.1 , 0.15 , 1) ,
242 size_hint =(1 , 1)
243 )
244 notif_top = MDBoxLayout ( orientation =" horizontal ", size_hint_y = None ,
height ="30 dp")
245 notif_title = MDLabel (
246 text =" Recent Notifications ",
247 font_style =" Subtitle2 ",
248 theme_text_color =" Custom ",
249 text_color =(0.5 , 0.7 , 1, 1)
250 )
251 self . clear_button = MDRaisedButton (
252 text =" Clear ",
253 md_bg_color =(0.5 , 0.1 , 0.1 , 1) ,
254 font_size ="12 sp",
255 on_release = self . clear_notifications ,
256 size_hint =( None , None ) ,
257 height ="28 dp",
258 width ="80 dp",
259 pos_hint ={" center_y ": 0.5}
260 )
261 notif_top . add_widget ( notif_title )
262 notif_top . add_widget ( Widget () ) # Spacer
263 notif_top . add_widget ( self . clear_button )
264
265 self . scroll = ScrollView (
266 size_hint =(1 , 1) ,
267 do_scroll_x = False # Only vertical scrolling
268 )
269
270 self . notif_container = MDBoxLayout (
271 orientation =" vertical ",
272 spacing =8 ,
273 padding =[5 , 10] ,
274 size_hint_y = None
275 )
276 self . notif_container . bind (
277 minimum_height = self . notif_container . setter ('height ')
278 )
279 self . scroll . add_widget ( self . notif_container )
280
281 self . notification_card . add_widget ( notif_top )
282 self . notification_card . add_widget ( self . scroll )
283 self . add_widget ( self . notification_card )
284
285 # Firebase variables
286 self . last_lock_status = ""
287 self . last_package_status = ""
288 self . vibration_counter = 0
289 self . vibration_last_time = 0
290
291 # Start checking Firebase regularly
292 Clock . schedule_interval ( self . safe_check_status , 5)
293 def safe_check_status ( self , dt ) :
294 threading . Thread ( target = self . _check_status_thread ). start ()
295
296 def clear_notifications ( self , * args ):
297 self . notifications . clear ()
298 self . notif_container . clear_widgets ()
299
300 def _check_status_thread ( self ):
301 try :
302 data = db . child (" guardbox "). get () . val ()
303 if data :
304 Clock . schedule_once ( lambda dt : self . update_status ( data ))
305 except Exception as e:
306 print (" Firebase error :", e )
307
308 def add_notification ( self , message , icon_path ):
309 if len ( self . notifications ) >= 5:
310 self . notifications . pop (0)
311 self . notif_container . clear_widgets ()
312
313 self . notifications . append (( message , icon_path ))
314
315 notif_row = MDBoxLayout (
316 orientation =" horizontal ",
317 spacing =10 ,
318 size_hint_y = None ,
319 height ="40 dp",
320 padding =[5 , 5] ,
321 )
322
323 notif_icon = Image (
324 source = icon_path ,
325 size_hint =( None , None ) ,
326 size =("30 dp", "30 dp") ,
327 )
328
329 notif_text = MDLabel (
330 text = message ,
331 theme_text_color =" Custom ",
332 text_color =(1 , 1 , 1, 1) ,
333 font_style =" Body1 ",
334 halign =" left ",
335 valign =" middle ",
336 )
337
338 notif_row . add_widget ( notif_icon )
339 notif_row . add_widget ( notif_text )
340
341 self . notif_container . add_widget ( notif_row )
342
343
344 def update_status ( self , data ):
345 locked = data . get (" locked ", False )
346 weight = data . get (" weight ", 0)
347 vibration = data . get (" vibration ", False )
348
349 lock_text = " Locked " if locked else " Unlocked "
350 package_text = " Package Detected " if weight >= WEIGHT_THRESHOLD else
" Box Empty "
351
352 # Update Lock Status
353 if lock_text != self . last_lock_status :
354 self . last_lock_status = lock_text
355 icon = " locked . png " if locked else " unlocked . png "
356 self . add_notification (" GuardBox Locked " if locked else " GuardBox
Unlocked ", icon )
357
358 if locked :
359 self . show_locked ()
360 else :
361 self . show_unlocked ()
362
363 self . lock_status . text = lock_text
364 self . lock_image . source = icon
365
366 if locked :
367 self . lock_status . text_color = (1 , 0.4 , 0.4 , 1) # Red
368 else :
369 self . lock_status . text_color = (0.1 , 1 , 0.1 , 1) # Green
370
371 # Update Package Status
372 if package_text != self . last_package_status :
373 self . last_package_status = package_text
374
375 if weight >= WEIGHT_THRESHOLD :
376 self . add_notification (" Package detected ", " box . png ")
377 self . show_cargo_true ()
378 else :
379 self . add_notification ("No package detected ", "box. png ")
380 self . show_cargo_false ()
381
382 self . status_label . text = package_text
383 # Vibration Detection and Alerts
384 now = time . time ()
385 if vibration :
386 if now - self . vibration_last_time > 10:
387 self . vibration_counter = 0 # reset counter if time gap too big
388
389 self . vibration_counter += 1
390 self . vibration_last_time = now
391
392 if self . vibration_counter < 3:
393 self . add_notification (" Vibration detected !", " alert .png")
394 self . show_vibration_alert ()
395 elif self . vibration_counter == 3:
396 self . add_notification (" Multiple vibrations detected ! Possible
tampering !", " alert . png ")
397 self . show_special_vibration_alert ()
398 def show_vibration_alert ( self ):
399 notification . notify (
400 title =" GuardBox Alert ",
401 message =" Vibration detected !",
402 timeout =5
403 )
404
405 def show_special_vibration_alert ( self ) :
406 notification . notify (
407 title =" GuardBox Critical Alert ",
408 message =" Multiple vibrations detected ! Immediate check recommended !",
409 timeout =7
410 )
411
412 def show_cargo_true ( self ):
413 notification . notify (
414 title =" Package placed .",
415 message =" Your package has been placed inside the GuardBox .",
416 timeout =5
417 )
418
419 def show_cargo_false ( self ):
420 notification . notify (
421 title =" Package is taken .",
422 message ="The GuardBox is now empty .",
423 timeout =5
424 )
425
426 def show_locked ( self ):
427 notification . notify (
428 title =" GuardBox Locked ",
429 message ="The GuardBox has been securely locked .",
430 timeout =5
431 )
432
433 def show_unlocked ( self ):
434 notification . notify (
435 title =" GuardBox Unlocked ",
436 message ="The GuardBox has been unlocked .",
437 timeout =5
438 )
439 def send_command ( self , cmd ):
440 def run () :
441 try :
442 if cmd == " lock ":
443 db . child (" guardbox "). update ({" locked ": True })
444 else :
445 db . child (" guardbox "). update ({" locked ": False })
446 # After sending a command , refresh status
447 Clock . schedule_once ( lambda dt : self . safe_check_status (0) )
448 except Exception as e:
449 print (" Command error :", e)
450
451 threading . Thread ( target = run ) . start ()
452 class GuardBoxApp ( MDApp ):
453 def build ( self ):
454 self . theme_cls . theme_style = " Dark "
455 self . theme_cls . primary_palette = " BlueGray "
456 return MainScreen ()
457
458
459 if __name__ == '__main__ ':
460 GuardBoxApp () . run ()
