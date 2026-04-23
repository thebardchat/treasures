What's New in Open WebUI

Release Notes
v0.7.2
v0.7.2 - 2026-01-10
fixed
⚡ Users no longer experience database connection timeouts under high concurrency due to connections being held during LLM calls, telemetry collection, and file status streaming. #20545, #20542, #20547
📝 Users can now create and save prompts in the workspace prompts editor without encountering errors. Commit
🎙️ Users can now use local Whisper for speech-to-text when STT_ENGINE is left empty (the default for local mode). #20534
📊 The Evaluations page now loads faster by eliminating duplicate API calls to the leaderboard and feedbacks endpoints. Commit
🌐 Fixed missing Settings tab i18n label keys. #20526
v0.7.1 - 2026-01-09
fixed
⚡ Improved reliability for low-spec and SQLite deployments. Fixed page timeouts by disabling database session sharing by default, improving stability for resource-constrained environments. Users can re-enable via 'DATABASE_ENABLE_SESSION_SHARING=true' if needed. #20520
v0.7.0 - 2026-01-09
added
🤖 Native Function Calling with Built-in Tools. Users can now ask models to perform multi-step tasks that combine web research, knowledge base queries, note-taking, and image generation in a single conversation—for example, "research the latest on X, save key findings to a note, and generate an infographic." Requires models with native function calling support and function calling mode set to "Native" in Chat Controls. #19397, Commit
🧠 Users can now ask the model to find relevant context from their notes, past chats, and channel messages—for example, "what did I discuss about project X last week?" or "find the conversation where I brainstormed ideas for Y." Commit
📚 Users can now ask the model to search their knowledge bases and retrieve documents without manually attaching files—for example, "find the section about authentication in our API docs" or "what do our internal guidelines say about X?" Commit
💭 Users with models that support interleaved thinking now get more refined results from multi-step workflows, as the model can analyze each tool's output before deciding what to do next.
🔍 When models invoke web search, search results appear as clickable citations in real-time for full source verification. Commit
🎚️ Users can selectively disable specific built-in tools (timestamps, memory, chat history, notes, web search, knowledge bases) per model via the model editor's capabilities settings. Commit
👁️ Pending tool calls are now displayed during response generation, so users know which tools are being invoked. Commit
📁 Administrators can now limit the number of files that can be uploaded to folders using the "FOLDER_MAX_FILE_COUNT" setting, preventing resource exhaustion from bulk uploads. #19810, Commit, Commit
⚡ Users experience transformative speed improvements across the entire application through completely reengineered database connection handling, delivering noticeably faster page loads, butter-smooth interactions, and rock-solid stability during intensive operations like user management and bulk data processing. Commit, Commit, Commit, Commit, Commit, Commit
🚀 Users experience significantly faster initial page load times through dynamic loading of document processing libraries, reducing the initial bundle size. #20200, #20202, #20203, #20204
💨 Administrators experience dramatically faster user list loading through optimized database queries that eliminate N+1 query patterns, reducing query count from 1+N to just 2 total queries regardless of user count. #20427
📋 Notes now load faster through optimized database queries that batch user lookups instead of fetching each note's author individually. Commit
💬 Channel messages, pinned messages, and thread replies now load faster through batched user lookups instead of individual queries per message. #20458, #20459, #20460
🔗 Users can now click citation content links to jump directly to the relevant portion of source documents with automatic text highlighting, making it easier to verify AI responses against their original sources. #20116, Commit
📌 Users can now pin or hide models directly from the Workspace Models page and Admin Settings Models page, making it easier to manage which models appear in the sidebar without switching to the chat interface. #20176
🔎 Administrators can now quickly find settings using the new search bar in the Admin Settings sidebar, which supports fuzzy filtering by category names and related keywords like "whisper" for Audio or "rag" for Documents. #20434
🎛️ Users can now view read-only models in the workspace models list, with clear "Read Only" badges indicating when editing is restricted. #20243, #20369
📝 Users can now view read-only prompts in the workspace prompts list, with clear "Read Only" badges indicating when editing is restricted. #20368
🔧 Users can now view read-only tools in the workspace tools list, with clear "Read Only" badges indicating when editing is restricted. #20243, #20370
📂 Searching for files is now significantly faster, especially for users with large file collections. Commit
🏆 The Evaluations leaderboard now calculates Elo ratings on the backend instead of in the browser, improving performance and enabling topic-based model ranking through semantic search. #15392, #20476, Commit
📊 The Evaluations leaderboard now includes a per-model activity chart displaying daily wins and losses as a diverging bar chart, with 30-day, 1-year, and all-time views using weekly aggregation for longer timeframes.
🎞️ Users can now upload animated GIF and WebP formats as model profile images, with animation preserved by skipping resize processing for these file types. Commit
📸 Users uploading profile images for users, models, and arena models now benefit from WebP compression at 80% quality instead of JPEG, resulting in significantly smaller file sizes and faster uploads while maintaining visual quality. Commit
⭐ Action Function developers can now update message favorite status using the new "chat:message:favorite" event, enabling the development of pin/unpin message actions without race conditions from frontend auto-save. #20375
🌐 Users with OpenAI-compatible models that have web search capabilities now see URL citations displayed as sources in the interface. #20172, Commit
📰 Users can now dismiss the "What's New" changelog modal permanently using the X button, matching the behavior of the "Okay, Let's Go!" button. #20258
📧 Administrators can now configure the admin contact email displayed in the Account Pending overlay directly from the Admin Panel instead of only through environment variables. #12500, #20260
📄 Administrators can now enable markdown header text splitting as a preprocessing step that works with either character or token splitting, through the new "ENABLE_MARKDOWN_HEADER_TEXT_SPLITTER" setting. Commit, Commit, Commit
🧩 Administrators can now set a minimum chunk size target using the "CHUNK_MIN_SIZE_TARGET" setting to merge small markdown header chunks with neighbors, which improves retrieval quality by eliminating tiny meaningless fragments, significantly speeds up document processing and embedding, reduces storage costs, and lowers embedding API costs or local compute requirements. #19595, #20314, Commit
💨 Administrators can now enable KV prefix caching optimization by setting "RAG_SYSTEM_CONTEXT" to true, which injects RAG context into the system message instead of user messages, enabling models to reuse cached tokens for follow-up questions instead of reprocessing the entire context on each turn, significantly improving response times and reducing costs for cloud-based models. #20301, #20317
🖼️ Administrators and Action developers can now control image generation denoising steps per-request using a steps parameter, allowing Actions and API calls to override the global IMAGE_STEPS configuration for both ComfyUI and Automatic1111 engines. #20337
🗄️ Administrators running multi-pod deployments can now designate a master pod to handle database migrations using the "ENABLE_DB_MIGRATIONS" environment variable. Commit
🎙️ Administrators can now configure Whisper's compute type using the "WHISPER_COMPUTE_TYPE" environment variable to fix compatibility issues with CUDA/GPU deployments. Commit
🔍 Administrators can now control sigmoid normalization for CrossEncoder reranking models using the "SENTENCE_TRANSFORMERS_CROSS_ENCODER_SIGMOID_ACTIVATION_FUNCTION" environment variable, enabled by default for proper relevance threshold behavior with MS MARCO models. #20228
🔒 Administrators can now disable SSL certificate verification for external tools using the "REQUESTS_VERIFY" environment variable, enabling integration with self-signed certificates for Tika, Ollama embeddings, and external rerankers. #19968, Commit
📈 Administrators can now control audit log output destinations using "ENABLE_AUDIT_STDOUT" and "ENABLE_AUDIT_LOGS_FILE" environment variables, allowing audit logs to be sent to container logs for centralized logging systems. #20114, Commit
🛡️ Administrators can now restrict non-admin user access to Interface Settings through per-user or per-group permissions. #20424
🧠 Administrators can now globally enable or disable the Memories feature and control access through per-user or per-group permissions, with the Personalization tab automatically hidden when the feature is disabled. #20462
🟢 Administrators can now globally enable or disable user status visibility through the "ENABLE_USER_STATUS" setting in Admin Settings. #20488
🪝 Channel managers can now create webhooks to allow external services to post messages to channels without authentication. Commit
📄 In the model editor users can now disable the "File Context" capability to skip automatic file content extraction and injection, forwarding raw messages with file attachment metadata instead for use with custom tools or future built-in file access tools. Commit, Docs:Commit
🔊 In the model editor users can now configure a specific TTS voice for each model, overriding user preferences and global defaults to give different AI personas distinct voices. #3097, Commit
👥 Administrators now have three granular group sharing permission options instead of a simple on/off toggle, allowing them to choose between "No one", "Members", or "Anyone" for who can share content to each group. Commit
📦 Administrators can now export knowledge bases as zip files containing text files for backup and archival purposes. #20120, Commit
🚀 Administrators can now create an admin account automatically at startup via "WEBUI_ADMIN_EMAIL", "WEBUI_ADMIN_PASSWORD", and "WEBUI_ADMIN_NAME" environment variables, enabling headless and automated deployments without exposing the signup page. #17654, Commit
🦆 Administrators can now select a specific search backend for DDGS instead of random selection, with options including Bing, Brave, DuckDuckGo, Google, Wikipedia, Yahoo, and others. #20330, #20366
🧭 Administrators can now configure custom Jina Search API endpoints using the "JINA_API_BASE_URL" environment variable, enabling region-specific deployments such as EU data processing. #19718, Commit
🔥 Administrators can now configure Firecrawl timeout values using the "FIRECRAWL_TIMEOUT" environment variable to control web scraping wait times. #19973, Commit
💾 Administrators can now use openGauss as the vector database backend for knowledge base document storage and retrieval. #20179
🔄 Various improvements were implemented across the application to enhance performance, stability, and security.
📊 Users can now sync their anonymous usage statistics to the Open WebUI Community platform to power community leaderboards, drive model evaluations, and contribute to open-source AI research that benefits everyone, all while keeping conversations completely private (only metadata like model names, message counts, and ratings are shared). By sharing your stats, you're helping the community identify which models perform best, contributing to transparent AI benchmarking, and supporting the collective effort to make AI better for all. You can also download your stats as JSON for personal analysis.
🌐 Translations for German, Portuguese (Brazil), Spanish, Simplified Chinese, Traditional Chinese, and Polish were enhanced and expanded.
fixed
🔊 Text-to-speech now correctly splits on newlines in addition to punctuation, so markdown bullet points and lists are spoken as separate sentences instead of being merged together. #5924, Commit
🔒 Users are now protected from stored XSS vulnerabilities in iFrame embeds for citations and response messages through configurable same-origin sandbox settings instead of hardcoded values. #20209, #20210
🔑 Image Generation, Web Search, and Audio (TTS/STT) API endpoints now enforce permission checks on the backend, closing a security gap where disabled features could previously be accessed via direct API calls. #20471
🛠️ Tools and Tool Servers (MCP and OpenAPI) now enforce access control checks on the backend, ensuring users can only access tools they have permission to use even via direct API calls. #20443, Commit
🔁 System prompts are no longer duplicated when using native function calling, fixing an issue where the prompt would be applied twice during tool-calling workflows. Commit
🗂️ Knowledge base uploads to folders no longer fail when "FOLDER_MAX_FILE_COUNT" is unset, fixing an issue where the default null value caused all uploads to error. Commit
📝 The "Create Note" button in the chat input now correctly hides for users without Notes permissions instead of showing and returning a 401 error when clicked. #20486, Commit
📊 The Evaluations page no longer crashes when administrators have large amounts of feedback data, as the leaderboard now fetches only the minimal required fields instead of loading entire conversation snapshots. #20476, #20489, Commit
💬 Users can now export chats, use the Ask/Explain popup, and view chat lists correctly again after these features were broken by recent refactoring changes that caused 500 and 400 server errors. #20146, #20205, #20206, #20212
💭 Users no longer experience data corruption when switching between chats during background operations like image generation, where messages from one chat would appear in another chat's history. #20266
🛡️ Users no longer encounter critical chat stability errors, including duplicate key errors from circular message dependencies, null message access during chat loading, and errors in the chat overview visualization. #20268
📡 Users with Channels no longer experience infinite recursion and connection pool exhaustion when fetching threaded replies, preventing RecursionError crashes during chat history loading. #20299, Commit
📎 Users no longer encounter TypeError crashes when viewing messages with file attachments that have undefined URL properties. #20343
🔐 Users with MCP integrations now experience reliable OAuth 2.1 token refresh after access token expiration through proper Protected Resource discovery, preventing integration failures that caused sessions to be deleted. #19794, #20138, #20291, Commit, Commit
📚 Users who belong to multiple groups can now see Knowledge Bases shared with those groups, fixing an issue where they would disappear when shared with more than one group. #20124, #20229, Commit
📂 Users now see the correct Knowledge Base name when hovering over # file references in chat input instead of "undefined". #20329, #20333
📋 Users now see notes displayed in correct chronological order within their time range groupings, fixing an issue where insertion order was not preserved. Commit
📑 Users collaborating on notes now experience proper content sync when initializing from both HTML and JSON formats, fixing sync failures in collaborative editing sessions. Commit
🔎 Users searching notes can now find hyphenated words and variations with spaces, so searching "todo" now finds "to-do" and "to do". Commit
📥 Users no longer experience false duplicate file warnings when reuploading files after initial processing failed, as the file hash is now only stored after successful processing completion. #19264, #20282, Commit
💾 Users experience significantly improved page load performance as model profile images now cache properly in browsers, avoiding unnecessary image refetches. Commit
🎨 Users can now successfully edit uploaded images instead of having new images generated, fixing an issue introduced by the file storage refactor where images with type "file" and content_type starting with "image/" weren't being recognized as editable images. #20237, #20169, #20239, Commit
🌐 Users writing in Persian and Arabic now see properly displayed right-to-left text in the notes section through automatic text direction detection. #19743, #20102, Commit
🤖 Users can now successfully @ mention models in Channels instead of experiencing silent failures. Commit
📋 Users on Windows now see correctly preserved line breaks when using the {{CLIPBOARD}} variable through CRLF to LF normalization. #19370, #20283
📁 Users now see the Knowledge Selector dropdown correctly displayed above the Create Folder modal instead of being hidden behind it. #20219, #20213
🌅 Users now see profile images in non-PNG formats like SVG, JPEG, and GIF displayed correctly instead of appearing broken. #20171
🆕 Non-admin users with disabled temporary chat permissions can now successfully create new chats and use pinned models from the sidebar. #20336, #20367, Commit
🎛️ Users can now successfully use workspace models in chat, fixing "Model not found" errors that occurred when using custom model presets. #20340, #20344, Commit, Commit
🔁 Users can now regenerate messages without crashes when the parent message is missing or corrupted in the chat history. #20264
✏️ Users no longer experience TipTap rich text editor crashes with "editor view is not available" errors when plugins or async methods try to access the editor after it has been destroyed. #20266
📗 Administrators with bypass access control enabled now correctly have write access to all knowledge bases. #20371
🔍 Administrators using local CrossEncoder reranking models now see proper relevance threshold behavior through MS MARCO model score normalization to the 0-1 range via sigmoid activation. #19999, #20228
🎯 Administrators using local SentenceTransformers embedding engine now benefit from proper batch size settings, preventing excessive memory usage from the default batch size of 32. #20053, #20054, Commit
🔧 Administrators and users in offline mode or restricted environments like uv, poetry, and NixOS no longer experience crashes when Tools and Functions have frontmatter requirements, as pip installation is now skipped when offline mode is enabled. #20320, #20321, Commit
📄 Administrators can now properly configure the MinerU document parsing service as the MinerU Cloud API key field is now available in the Admin Panel Documents settings. #20319, #20328
⚠️ Administrators no longer see SyntaxWarnings for invalid escape sequences in password validation regex patterns. #20298, Commit
🎨 Users with ComfyUI workflows now see only the intended final output images in chat instead of duplicate images from intermediate processing nodes like masks, crops, or segmentation previews. #20158, #20182
🖼️ Users with image generation enabled no longer see false vision capability warnings, allowing them to send follow-up messages after generating images and to send images to non-vision models for image editing. #20129, #20256
🔌 Administrators no longer experience infinite loading screens when invalid or MCP-style configurations are used with OpenAPI connection types for external tools. #20207, #20257
📥 Administrators no longer encounter TypeError crashes during SHA256 verification when uploading GGUF models via URL, fixing 500 Internal Server Error crashes. #20263
🚦 Users with Brave Search now experience automatic retry with a 1-second delay when hitting rate limits, preventing failures when sequential requests exceed the 1 request per second limit, though this only works reliably when web search concurrency is set to a maximum of 1. #15134, #20255
🗄️ Administrators with Redis Sentinel deployments no longer experience crashes during websocket disconnections due to improper async-generator handling in the YDocManager. #20142, #20145
🔐 Administrators using SCIM group management no longer encounter 500 errors when working with groups that have no members. #20187
🔗 Users now experience more reliable citations from AI models, especially when using smaller or weaker models that may not format citation references perfectly. Commit
🕸️ Administrators can now successfully save WebSearch settings without encountering validation errors for domain filter lists, YouTube language settings, or timeout values. #20422
📦 Administrators installing with the uv package manager now experience successful installation after deprecated dependencies that were causing conflicts were removed. #20177, #20192
⏱️ Administrators using custom "AIOHTTP_CLIENT_TIMEOUT" settings now see the configured timeout correctly applied to embedding generation, OAuth discovery, webhook calls, and tool/function loading instead of falling back to the default 300-second timeout. Commit
changed
⚠️ This release includes a major overhaul of database connection handling in the backend that requires all instances in multi-worker, multi-server, or load-balanced deployments to be updated simultaneously; running mixed versions will cause failures due to incompatible database connection management between old and new instances.
📝 Administrators who previously used the standalone "Markdown (Header)" text splitter must now switch to "character" or "token" mode with the new "ENABLE_MARKDOWN_HEADER_TEXT_SPLITTER" toggle enabled, as document chunking now applies markdown header splitting as a preprocessing step before character or token splitting. Commit, Commit, Commit
🖼️ Users no longer see the "Generate Image" action button in chat message interfaces; custom function should be used. Commit
🔗 Administrators will find the Admin Evaluations page at the new URL "/admin/evaluations/feedback" instead of "/admin/evaluations/feedbacks" to use the correct uncountable form of the word. #20296
🔐 Scripts or integrations that directly called Image Generation, Web Search, or Audio APIs while those features were disabled in the Admin UI will now receive 403 Forbidden errors, as backend permission enforcement has been added to match frontend restrictions. #20471
👥 The default group sharing permission changed from "Members" to "Anyone", meaning users can now share content to any group configured with "Anyone" permission regardless of their membership in that group. Commit
v0.6.43 - 2025-12-22
fixed
🐍 Python dependency installation issues were resolved by correcting pip dependency handling, preventing installation failures in certain environments and improving setup reliability. Commit
🎙️ Speech-to-Text default content type handling was fixed and refactored to ensure correct MIME type usage, improving compatibility across STT providers and preventing transcription errors caused by incorrect defaults. Commit
🖼️ Temporary chat image handling was fixed and refactored, ensuring images generated or edited in temporary chats are correctly processed, stored, and displayed without inconsistencies or missing references. Commit
🎨 Image action button fixed, restoring the ability to trigger image generation, editing, and related image actions from the chat UI. Commit
v0.6.42 - 2025-12-21
added
📚 Knowledge base file management was overhauled with server-side pagination loading 30 files at a time instead of loading entire collections at once, dramatically improving performance and responsiveness for large knowledge bases with hundreds or thousands of files, reducing initial load times and memory usage while adding server-side search and filtering, view options for files added by the user versus shared files, customizable sorting by name or date, and file authorship tracking with upload timestamps. Commit
✨ Knowledge base file management was enhanced with automatic list refresh after file operations ensuring immediate UI updates, improved permission validation at the model layer, and automatic channel-file association for files uploaded with channel metadata. Commit
🔎 Knowledge command in chat input now uses server-side search for massive performance increases when selecting knowledge bases and files. Commit
🗂️ Knowledge workspace listing now uses server-side pagination loading 30 collections at a time with new search endpoints supporting query filtering and view options for created versus shared collections. Commit
📖 Knowledge workspace now displays all collections with read access including shared read-only collections, enabling users to discover and explore knowledge bases they don't own while maintaining proper access controls through visual "Read Only" badges and automatically disabled editing controls for name, description, file uploads, content editing, and deletion operations. Commit
📁 Bulk website and YouTube video attachment now supports adding multiple URLs at once (newline-separated) with automatic YouTube detection and transcript retrieval, processed sequentially to prevent resource strain, and both websites and videos can now be added directly to knowledge bases through the workspace UI. Commit, #6202, #19587, #8231
🪟 Sidebar width is now resizable on desktop devices with persistent storage in localStorage, enforcing minimum and maximum width constraints (220px to 480px) while all layout components now reference the dynamic sidebar width via CSS variables for consistent responsive behavior. Commit
📝 Notes feature now supports server-side search and filtering with view options for notes created by the user versus notes shared with them, customizable sorting by name or date in both list and grid view modes within a redesigned interface featuring consolidated note management controls in a unified header, group-based permission sharing with read, write, and read-only access control displaying note authorship and sharing status for better collaboration, and paginated infinite scroll for improved performance with large note collections. Commit
👁️ Notes now support read-only access permissions, allowing users to share notes for viewing without granting edit rights, with the editor automatically becoming non-editable and appropriate UI indicators when read-only access is detected. Commit
📄 Notes can now be created directly from the chat input field, allowing users to save drafted messages or content as notes without navigation or retyping. Commit
🪟 Sidebar folders, channels, and pinned models sections now automatically expand when creating new items or pinning models, providing immediate visual feedback for user actions. Commit, #19929
📋 Chat file associations are now properly tracked in the database through a new "chat_file" table, enabling accurate file management across chats and ensuring proper cleanup of files when chats are deleted, while improving database consistency in multi-node deployments. Commit
🖼️ User-uploaded images are now automatically converted from base64 to actual file storage on the server, eliminating large inline base64 strings from being stored in chat history and reducing message payload sizes while enabling better image management and sharing across multiple chats. Commit
📸 Shared chats with generated or edited images now correctly display images when accessed by other users by properly linking generated images to their chat and message through the chat_file table, ensuring images remain accessible in shared chat links. Commit, #19393
📊 File viewer modal was significantly enhanced with native-like viewers for Excel/CSV spreadsheets rendering as interactive scrollable tables with multi-sheet navigation support, Markdown documents displaying with full typography including headers, lists, links, and tables, and source code files showing syntax highlighting, all accessible through a tabbed interface defaulting to raw text view. #20035, #2867
📏 Chat input now displays an expand button in the top-right corner when messages exceed two lines, providing optional access to a full-screen editor for composing longer messages with enhanced workspace and visibility while temporarily disabling the main input to prevent editing conflicts. Commit
💬 Channel message data lazy loading was implemented, deferring attachment and file metadata retrieval until needed to improve initial message list load performance. Commit
🖼️ Channel image upload handling was optimized to process and store compressed images directly as files rather than inline data, improving memory efficiency and message load times. Commit
🎥 Video file playback support was added to channel messages, enabling inline video viewing with native player controls. Commit
🔐 LDAP authentication now supports user entries with multiple username attributes, correctly handling cases where the username field contains a list of values. Commit, #19878
👨‍👩‍👧‍👦 The "ENABLE_PUBLIC_ACTIVE_USERS_COUNT" environment variable now allows restricting active user count visibility to administrators, reducing backend load and addressing privacy concerns in large deployments. #20027, #13026
🚀 Models page search input performance was optimized with a 300ms debounce to reduce server load and improve responsiveness. #19832
💨 Frontend performance was optimized by preventing unnecessary API calls for API Keys and Channels features when they are disabled in admin settings, reducing backend noise and improving overall system efficiency. #20043, #19967
📎 Channel file association tracking was implemented, automatically linking uploaded files to their respective channels with a dedicated association table enabling better organization and future file management features within channels. Commit
👥 User profile previews now display group membership information for easier identification of user roles and permissions. Commit
🌍 The "SEARXNG_LANGUAGE" environment variable now allows configuring search language for SearXNG queries, replacing the hardcoded "en-US" default with a configurable setting that defaults to "all". #19909
⏳ The "MINERU_API_TIMEOUT" environment variable now allows configuring request timeouts for MinerU document processing operations. #20016, #18495
🔧 The "RAG_EXTERNAL_RERANKER_TIMEOUT" environment variable now allows configuring request timeouts for external reranker operations. #20049, #19900
🎨 OpenAI GPT-IMAGE 1.5 model support was added for image generation and editing with automatic image size capabilities. Commit
🔑 The "OAUTH_AUDIENCE" environment variable now allows OAuth providers to specify audience parameters for JWT access token generation. #19768
⏰ The "REDIS_SOCKET_CONNECT_TIMEOUT" environment variable now allows configuring socket connection timeouts for Redis and Sentinel connections, addressing potential failover and responsiveness issues in distributed deployments. #19799, Docs:#882
⏱️ The "WEB_LOADER_TIMEOUT" environment variable now allows configuring request timeouts for SafeWebBaseLoader operations. #19804, #19734
🚀 Models API endpoint performance was optimized through batched model loading, eliminating N+1 queries and significantly reducing response times when filtering models by user permissions. Commit
🔀 Custom model fallback handling was added, allowing workspace-created custom models to automatically fall back to the default chat model when their configured base model is not found; set "ENABLE_CUSTOM_MODEL_FALLBACK" to true to enable, preventing workflow disruption when base models are removed or renamed, while ensuring other requests remain unaffected. Commit, #19985
📡 A new /feedbacks/all/ids API endpoint was added to return only feedback IDs without metadata, significantly improving performance for external integrations working with large feedback collections. Commit
📈 An experimental chat usage statistics endpoint (GET /api/v1/chats/stats/usage) was added with pagination support (50 chats per page) and comprehensive per-chat analytics including model usage counts, user and assistant message breakdowns, average response times calculated from message timestamps, average content lengths, and last activity timestamps; this endpoint remains experimental and not suitable for production use as it performs intensive calculations by processing entire message histories for each chat without caching. Commit
🔄 Various improvements were implemented across the frontend and backend to enhance performance, stability, and security.
🌐 Translations for German, Danish, Finnish, Korean, Portuguese (Brazil), Simplified Chinese, Traditional Chinese, Catalan, and Spanish were enhanced and expanded.
fixed
⚡ External reranker operations were optimized to prevent event loop blocking by offloading synchronous HTTP requests to a thread pool using asyncio.to_thread(), eliminating application freezes during RAG reranking queries. #20049, #19900
💭 Text loss in the explanation feature when using the "CHAT_STREAM_RESPONSE_CHUNK_MAX_BUFFER_SIZE" environment variable was resolved by correcting newline handling in streaming responses. #19829
📚 Knowledge base batch file addition failures caused by Pydantic validation errors are now prevented by making the meta field optional in file metadata responses, allowing files without metadata to be processed correctly. #20022, #14220
🗄️ PostgreSQL null byte insertion failures when attaching web pages or processing embedded content are now prevented by consolidating text sanitization logic across chat messages, web search results, and knowledge base documents, removing null bytes and invalid UTF-8 surrogates before database insertion. #20072, #19867, #18201, #15616
🎫 MCP OAuth 2.1 token exchange failures are now fixed by removing duplicate credential passing that caused "ID1,ID1" concatenation and 401 errors from the token endpoint. #20076, #19823
📝 Notes "Improve" action now works correctly after the streaming API change in v0.6.41 by ensuring uploaded files are fully retrieved with complete metadata before processing, restoring note improvement and summarization functionality. Commit, #20078
🔑 MCP OAuth 2.1 tool servers now work correctly in multi-node deployments through lazy-loading of OAuth clients from Redis-synced configuration, eliminating 404 errors when load balancers route requests to nodes that didn't process the original config update. #20076, #19902, #19901
🧩 Chat loading failures when channels permissions were disabled are now prevented through graceful error handling. Commit
🔍 Search bar freezing and crashing issues in Models, Chat, and Archived Chat pages caused by excessively long queries exceeding server URL limits were resolved by truncating queries to 500 characters, and knowledge base layout shifting with long names was fixed by adjusting flex container properties. #19832
🎛️ Rate limiting errors (HTTP 429) with Brave Search free tier when generating multiple queries are now prevented through asyncio.Semaphore-based concurrency control applied globally to all search engines. #20070, #20003, #14107, #15134
💥 UI crashes and white screen errors caused by null chat lists during loading or network failures were prevented by adding null safety checks to chat iteration in folder placeholders and archived chat modals. #19898
🧩 Chat overview tab crashes caused by undefined model references were resolved by adding proper null checks when accessing deleted or ejected models. #19935
🔄 MultiResponseMessages component crashes when navigating chat history after removing or changing selected models are now prevented through proper component re-initialization. Commit, #18599
🚫 Channel API endpoint access is now correctly blocked when channels are globally disabled, preventing users with channel permissions from accessing channel data via API requests when the feature is turned off in admin settings. #19957, #19914
👤 User list popup display in the admin panel was fixed to correctly track user identity when sorting or filtering changes the list order, preventing popups from showing incorrect user information. Commit, #20046
👥 User selection in the "Edit User Group" modal now preserves pagination position, allowing administrators to select multiple users across pages without resetting to page 1. #19959
📸 Model avatar images now update immediately in the admin models list through proper Cache-Control headers, eliminating the need for manual cache clearing. #19959
🔒 Temporary chat permission enforcement now correctly prevents users from enabling the feature through personal settings when disabled in default or group permissions. #19785
🎨 Image editing with reference images now correctly uses both previously generated images and newly uploaded reference images. Commit
🧠 Image generation and editing operations are now explicitly injected into system context, improving LLM comprehension even for weaker models so they reliably acknowledge operations instead of incorrectly claiming they cannot generate images. Commit
📑 Source citation rendering errors when citation syntax appeared in user messages or contexts without source data were resolved. Commit
📄 DOCX file parsing now works correctly in temporary chats through client-side text extraction, preventing raw data from being displayed. Commit
🔧 Pipeline settings save failures when valve properties contain null values are now handled correctly. #19791
⚙️ Model usage settings are now correctly preserved when switching between models instead of being unexpectedly cleared or reset. #19868, #19549
🛡️ Invalid PASSWORD_VALIDATION_REGEX_PATTERN configurations no longer cause startup warnings, with automatic fallback to the default pattern when regex compilation fails. #20058
🎯 The DefaultFiltersSelector component in model settings now correctly displays when only global toggleable filters are present, enabling per-model default configuration. #20066
🎤 Audio file upload failures caused by MIME type matching issues with spacing variations and codec parameters were resolved by implementing proper MIME type parsing. #17771, #17761
⌨️ Regenerate response keyboard shortcut now only activates when chat input is selected, preventing unintended regeneration when modals are open or other UI elements are focused. #19875
📋 Log truncation issues in Docker deployments during application crashes were resolved by disabling Python stdio buffering, ensuring complete diagnostic output is captured. #19844
🔴 Redis cluster compatibility issues with disabled KEYS command were resolved by replacing blocking KEYS operations with production-safe SCAN iterations. #19871, #15834
🔤 File attachment container layout issues when using RTL languages were resolved by applying chat direction settings to file containers across all message types. #19891, #19742
🔃 Ollama model list now automatically refreshes after model deletion, preventing deleted models from persisting in the UI and being inadvertently re-downloaded during subsequent pull operations. #19912
🌐 Ollama Cloud web search now correctly applies domain filtering to search results. Commit
📜 Tool specification serialization now preserves non-ASCII characters including Chinese text, improving LLM comprehension and tool selection accuracy by avoiding Unicode escape sequences. #19942
🛟 Model editor stability was improved with null safety checks for tools, functions, and file input operations, preventing crashes when stores are undefined or file objects are invalid. #19939
🗣️ MoA completion handling stability was improved with null safety checks for response objects, boolean casting for settings, and proper timeout type definitions. #19921
🎛️ Chat functionality failures caused by empty logit_bias parameter values are now prevented by properly handling empty strings in the parameter parsing middleware. #19982
🔏 Administrators can now delete read-only knowledge bases from deleted users, resolving permission issues that previously prevented cleanup of orphaned read-only content. Commit
💾 Cloned prompts and tools now correctly preserve their access control settings instead of being reset to null, preventing unintended visibility changes when duplicating private or restricted items. #19960, #19360
🎚️ Text scale adjustment buttons in Interface Settings were fixed to correctly increment and decrement the scale value. #19699
🎭 Group channel invite button text visibility in light theme was corrected to display properly against dark backgrounds. #19828
📁 The move button is now hidden when no folders exist, preventing display of non-functional controls. #19705
📦 Qdrant client dependency was updated to resolve startup version incompatibility warnings. #19757
🧮 The "ENABLE_ASYNC_EMBEDDING" environment variable is now correctly applied to embedding operations when configured exclusively via environment variables. #19748
🌄 The "COMFYUI_WORKFLOW_NODES" and "IMAGES_EDIT_COMFYUI_WORKFLOW_NODES" environment variables are now correctly loaded and parsed as JSON lists, and the configuration key name was corrected from "COMFYUI_WORKFLOW" to "COMFYUI_WORKFLOW_NODES". #19918, #19886
💫 Channel name length is now limited to 128 characters with validation to prevent display issues caused by excessively long names. Commit
🔐 Invalid PASSWORD_VALIDATION_REGEX_PATTERN configurations no longer cause startup warnings, with automatic fallback to the default pattern when regex compilation fails. #20058
🔎 Bocha search with filter list functionality now works correctly by returning results as a list instead of a dictionary wrapper, ensuring compatibility with result filtering operations. Commit, #19733
changed
⚠️ This release includes database schema changes; multi-worker, multi-server, or load-balanced deployments must update all instances simultaneously rather than performing rolling updates, as running mixed versions will cause application failures due to schema incompatibility between old and new instances.
📡 WEB_SEARCH_CONCURRENT_REQUESTS default changed from 10 to 0 (unlimited) — This setting now applies to all search engines instead of only DuckDuckGo; previously users were implicitly limited to 10 concurrent queries, but now have unlimited parallel requests by default; set to 1 for sequential execution if using rate-limited APIs like Brave free tier. #20070
💾 SQLCipher absolute path handling was fixed to properly support absolute database paths (e.g., "/app/data.db") instead of incorrectly stripping leading slashes and converting them to relative paths; this restores functionality for Docker volume mounts and explicit absolute path configurations while maintaining backward compatibility with relative paths. #20074
🔌 Knowledge base file listing API was redesigned with paginated responses and new filtering parameters; the GET /knowledge/{id}/files endpoint now returns paginated results with user attribution instead of embedding all files in the knowledge object, which may require updates to custom integrations or scripts accessing knowledge base data programmatically. Commit
🗑️ Legacy knowledge base support for deprecated document collections and tag-based collections was removed; users with pre-knowledge base documents must migrate to the current knowledge base system as legacy items will no longer appear in selectors or command menus. Commit
🔨 Source-level log environment variables (AUDIO_LOG_LEVEL, CONFIG_LOG_LEVEL, MODELS_LOG_LEVEL, etc.) were removed as they provided limited configuration options and added significant complexity across 100+ files; the GLOBAL_LOG_LEVEL environment variable, which already took precedence over source-level settings, now serves as the exclusive logging configuration method. #20045
🐍 LangChain was upgraded to version 1.2.0, representing a major dependency update and significant progress toward Python 3.13 compatibility while improving RAG pipeline functionality for document loading and retrieval operations. #19991