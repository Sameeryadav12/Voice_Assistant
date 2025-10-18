# Changelog

All notable changes to Sigma Voice Assistant will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-10-18

### 🎉 Initial Release

#### Added
- **Push-to-Talk Mode** - Reliable voice input with button control
- **Combined Mode** - Keyboard and voice input together
- **Hybrid Mode** - Keyboard-only input
- **8 Functional Skills** - Complete skill ecosystem
  - Info Skill (time, date, system info)
  - Reminder Skill (natural language reminders)
  - Recurring Reminder Skill
  - File Search Skill (graph-based search)
  - File Management Skill
  - App Launcher Skill (Chrome, CMD, Calculator, etc.)
  - System Control Skill
  - Help Skill

#### Features
- **Audio Processing**
  - Automatic sample rate detection and conversion
  - 28,000x audio boost for quiet microphones
  - Voice Activity Detection with WebRTC VAD
  - Noise filtering (ignores audio below threshold)
  - Audio resampling (44100Hz → 16000Hz)

- **Speech Recognition**
  - Google Speech Recognition integration
  - PocketSphinx offline recognition (disabled due to hallucinations)
  - Multi-engine support architecture
  - Confidence scoring
  - Cache system for improved performance

- **Wake Word System**
  - 14+ wake word variations for accent support
  - Trie-based O(m) keyword matching
  - Aho-Corasick multi-pattern matching
  - Fuzzy matching with Levenshtein distance

- **Intent Classification**
  - Hybrid ML approach
  - Rule-based + pattern matching
  - Entity extraction
  - Context awareness

- **Advanced Data Structures**
  - Trie for keyword matching
  - Priority Heap for task scheduling
  - LRU Cache for performance
  - Graph for file system navigation
  - Finite State Machine for dialogue

#### Fixed
- **Audio Pipeline**
  - Sample rate mismatch (44100Hz vs 16000Hz)
  - Audio too quiet for recognition (added aggressive boost)
  - Background noise false positives (improved VAD)
  - Continuous buffering without processing (added limits)
  - VAD detecting silence as speech (stricter thresholds)

- **Speech Recognition**
  - Missing sample_rate attribute in RecognitionConfig
  - Incorrect AudioData sample width
  - Sphinx hallucinating words from noise (disabled)
  - Google API timeout issues (better error handling)

- **Skills System**
  - Time queries not working (created InfoSkill)
  - "set reminder for X minutes" format not parsing (fixed regex)
  - File search queries with leading commas (better parsing)
  - Chrome not launching (added 3 installation paths)
  - CMD not opening (special handling)
  - Wake word leaving punctuation (improved cleaning)

- **User Experience**
  - Continuous listening capturing when user silent (fixed VAD)
  - Recognizing wrong words (added accent variations)
  - No feedback on what's being heard (added logging)
  - Confusing error messages (improved error handling)

#### Changed
- Default mode from continuous listening to push-to-talk
- Speech recognition from Sphinx-first to Google-only
- VAD aggressiveness from 0 to 3 (then back to smart detection)
- Energy threshold from 50 to 3000 (then to 500 with level check)
- Buffer size from 5 chunks to 20-50 chunks

#### Removed
- PocketSphinx as primary engine (kept as fallback)
- Strict audio level requirements (now accepts level 1+)
- Continuous buffering of silence
- Redundant test files

---

## [0.9.0] - Development Phase

### Added
- Initial project structure
- Basic voice recognition
- Core data structures
- Skill framework

---

## Future Versions

### [1.1.0] - Planned
- [ ] Whisper integration for offline recognition
- [ ] Voice training system
- [ ] Multi-language support
- [ ] TTS (Text-to-Speech) responses
- [ ] Cloud sync for reminders

### [1.2.0] - Planned
- [ ] macOS and Linux full support
- [ ] Web interface
- [ ] Mobile companion app
- [ ] Custom wake word training
- [ ] Voice analytics

---

## Version History Summary

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2025-10-18 | Initial release with push-to-talk |
| 0.9.0 | 2025-10-17 | Development phase |

---

## Migration Notes

### Upgrading to 1.0.0
- No migration needed for new installations
- If using custom audio configurations, check new AudioConfig defaults
- Push-to-talk is now recommended over continuous listening

---

## Breaking Changes

### Version 1.0.0
- Changed default recognition engine from Sphinx to Google
- Modified AudioConfig default values
- Renamed some internal functions (see API docs)

---

For more details on any version, see the [commit history](https://github.com/yourusername/voice_assistant/commits/main).

