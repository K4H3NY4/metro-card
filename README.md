# metro-card

METRO APP REST API END POINTS | CHEAT SHEET

Most routes require JWT token [Bearer \&lt;JWT\&gt;]

| Name | Method | Route | JSON | Protected |
| --- | --- | --- | --- | --- |
| Passenger End Points |
| Pass – Register | POST | _/pass/register_ | {&quot;first\_name&quot;:&quot; &quot;,&quot;last\_name&quot;:&quot; &quot;, &quot;email&quot;:&quot; &quot;,&quot;phone&quot;:&quot;2547xxxxx&quot;, &quot;password&quot;:&quot; &quot; } | N |
| Pass - Profile | GET | _/pass/profile_ | | Y |
| Pass – Balance | GET | _/pass/balance_ | | Y |
| Pass – Login | POST | _/pass/login_ | { &quot;email&quot;:&quot; &quot;, &quot;password&quot;:&quot; &quot; } | N |
| Pass – Edit Profile | PUT | _/pass/edit_ | { &quot;first\_name&quot;:&quot; &quot;, &quot;last\_name&quot;:&quot; &quot; } | Y |
| Pass – Top Up | POST | _/pass/topup_ | {&quot;amount&quot;:&quot;1000&quot;} | Y |
| Pass – Pay | POST | _/pay/pay_ | {&quot;reg\_no&quot;:&quot;KGD 123A&quot;,&quot;amount&quot;:&quot;120&quot;} | Y |
| Pass – Forgot Password | PUT | _/pass/forgot-password_ | { &quot;email&quot;:&quot; &quot;} | N |
| Pass – Change Password | PUT | _/pass/change-password_ | {&quot;new\_password&quot;:&quot; &quot;,&quot;confirm\_password&quot;:&quot; &quot;} | Y |
| Pass – All Payments | GET | _/pass/all-payments_ | | Y |
| Pass – All Top Ups | GET | _/pass/all-topup_ | | Y |
| Crew End Points |
| Crew - Register | POST | _/crew/register_ | { &quot;first\_name&quot;:&quot; &quot;, &quot;last\_name&quot;:&quot; &quot;, &quot;email&quot;:&quot; &quot;, &quot;phone&quot;:&quot;2547XXXX&quot;, &quot;password&quot;:&quot; &quot;} | N |
| Crew – Profile | GET | _/crew/profile_ | Y |
| Crew – Login | POST | _/crew/login_ | { &quot;email&quot;:&quot; &quot;, &quot;password&quot;:&quot; &quot;} | N |
| Crew – Forgot Password | PUT | _/crew/forgot-password_ | {&quot;email&quot;:&quot; &quot;} | N |
| Crew – Change Password | PUT | _/crew/change-password_ | {&quot;new\_password&quot;:&quot; &quot;, &quot;confirm\_password&quot;:&quot; &quot; } | Y |
| Crew – Edit Profile | PUT | _/crew/edit_ | { &quot;first\_name&quot;:&quot; &quot;, &quot;last\_name&quot;:&quot; &quot; } | Y |
| Crew – Add Bookmark | POST | _/crew/bookmark_ | { &quot;reg\_no&quot;:&quot; &quot;, &quot;alias&quot;:&quot; &quot; } | Y |
| Crew – View Bookmark | GET | _/crew/bookmark/\&lt;id\&gt;_ | Y |
| Crew – Pay using Bookmark | POST | _/crew/bookmark/\&lt;id\&gt;_ | { &quot;amount&quot;:&quot;80&quot;, &quot;pass\_phone&quot;:&quot;2547XXX&quot; } | Y |
| Crew – View All Bookmark | GET | _/crew/bookmark_ | { &quot;reg\_no&quot;:&quot;KGA 202X&quot;, &quot;alias&quot;:&quot; &quot; } | Y |
| Crew – View All Payments | GET | _/crew/payments_ | | Y |
| Crew – View Payments Per Car | GET | _/crew/payments/\&lt;id\&gt;_ | | Y |
| Owner End Points |
| Owner – Register | POST | _/owner/register_ | { &quot;first\_name&quot;:&quot; &quot;, &quot;last\_name&quot;:&quot; &quot;, &quot;email&quot;:&quot; &quot;, &quot;phone&quot;:&quot;254XXXX&quot;, &quot;password&quot;:&quot; &quot; } | N |
| Owner – Profile | GET | _/owner/profile_ | | Y |
| Owner – Login | POST | _/owner/login_ | { &quot;email&quot;:&quot; &quot;, &quot;password&quot;:&quot; &quot;} | N |
| Owner – Change Password | PUT | _/owner/change-password_ | { &quot;new\_password&quot;:&quot; &quot;, &quot;confirm\_password&quot;:&quot; &quot; } | Y |
| Owner – Forgot Password | PUT | _/owner/forgot-password_ | { &quot;email&quot;:&quot; &quot; } | N |
| Owner – Profile | GET | _/owner/profile_  | | Y |
| Owner – Edit Profile | PUT | _/owner/edit_ | { &quot;first\_name&quot;:&quot; &quot;, &quot;last\_name&quot;:&quot; &quot;} | Y |
| Owner – Add Vehicle | PUT | _/owner/add-vehicle_ | { &quot;reg\_no&quot;:&quot;KGA 200X&quot;, &quot;sacco&quot;:&quot; &quot;, &quot;capacity&quot;:&quot;33&quot; } | Y |
| Owner – View All Vehicle | GET | _/owner/vehicles_ |  | Y |
| Owner – View Vehicle | GET | _/owner/vehicle_ | { &quot;reg\_no&quot;:&quot;KGA 211X&quot;} | Y |
| Owner – Balance | GET | _/owner/balance_ | | Y |
| Owner – Withdraw | POST | _/owner/withdraw_ | { &quot;amount&quot;:&quot; &quot;, &quot;owner\_phone&quot;:&quot;2547XXXX&quot;} | Y |
| Owner – All Deposits | GET | _/owner/all-deposits_ | | Y |
| Owner – All Withdraw | GET | _/owner/all-withdraws_ | | Y |
| Owner – View Payments P. Car | GET | _/owner/vehicle/payment/\&lt;id\&gt;_ | | Y |
| Owner – Transfer | PUT | _/owner/transfer_ | { &quot;email&quot;:&quot; &quot;,&quot;reg\_no&quot;:&quot;KGA 200X&quot;} | Y |
| Owner – Edit Vehicle | PUT | _/owner/vehicle/1_ | {&quot;sacco&quot;:&quot; &quot;,&quot;capacity&quot;:&quot;14&quot;} | Y |
