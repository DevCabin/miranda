# Changelog

## [1.0.1] - 2024-03-19
### Added
- Voice interface with Web Speech API
- Modern ChatGPT-style UI
- Text-to-speech response capability
- Static file serving

### TODO
- [ ] Add logic to switch between Gemini search and database queries
- [ ] Implement more natural voice options for responses
- [ ] Enhance UI/UX:
  - [ ] Add chat history persistence
  - [ ] Improve message formatting
  - [ ] Add loading states/animations
  - [ ] Dark mode support
  - [ ] Mobile optimizations
- [ ] Add error handling for speech recognition
- [ ] Implement voice settings configuration

## [1.0.0] - 2024-03-19
### Added
- Initial stable release
- Working Gemini + Sheets integration
- Core API functionality
- Vercel deployment configuration

## [1.0.2] - 2024-03-19
### Security
- Added security notes to README
- Updated environment variable handling
### Fixed
- JSON parsing issues with service account credentials 

## [1.1.0] - 2024-03-XX
### Added
- Implemented Miranda's persona with defined personality traits
- Added personalized context for user (George)
- Enhanced prompt engineering for consistent personality
- Improved natural conversation flow with name usage

### Stable Features
- Voice interface integration
- Google Sheets data querying
- Personalized responses using Miranda's persona
- Natural conversation handling

### TODO
- Move persona configuration to separate config file to support multiple personas
- Implement persona switching mechanism 