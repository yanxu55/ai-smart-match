# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within SmartMatch, please send an email to the maintainer. All security vulnerabilities will be promptly addressed.

Please do not report security vulnerabilities through public GitHub issues.

## Security Considerations

### API Keys
- Never commit actual API keys to the repository
- Use `.env` files that are listed in `.gitignore`
- Rotate API keys regularly

### Data Privacy
- Student data is stored locally only
- No personal information is transmitted to external services except for AI processing
- Users should be aware that activity recommendations are generated using AI services

### Dependencies
- Regularly update dependencies to patch security vulnerabilities
- Use virtual environments for isolation
- Review third-party packages before installation
