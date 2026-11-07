# Gates: pymt5-linux

OWNS: pyproject.toml, src/**, tests/**, examples/**, scripts/**, .github/**, README.md, LICENSE, Dockerfile

Scope: Production-grade MetaTrader 5 SDK and drop-in replacement for Linux with Wine IPC bridge, remote gateway, mock simulator, and async streaming support.

- [x] G1: Package structure and pyproject.toml configuration validated
  CHECK: .venv/bin/pytest tests/test_package.py -k test_package_metadata -v
  EXPECT: test_package_metadata PASSED
  EVIDENCE: Verified. Hatchling build configuration and package metadata pass pytest.

- [x] G2: Complete MT5 constants, enums, data structures, and namedtuples specification
  CHECK: .venv/bin/pytest tests/test_constants_and_types.py -v -s
  EXPECT: ALL_TYPES_VALIDATED
  EVIDENCE: Verified. All timeframes, trade actions, order types, namedtuples, and structured dtypes pass.

- [x] G3: Protocol serialization, packet framing, and network transport
  CHECK: .venv/bin/pytest tests/test_protocol.py -v -s
  EXPECT: PROTOCOL_VALIDATED
  EVIDENCE: Verified. 4-byte header framing, JSON serialization, and socket roundtrip pass.

- [x] G4: Standalone Wine gateway and mock trading simulator engine
  CHECK: .venv/bin/pytest tests/test_mock_engine.py -v -s
  EXPECT: MOCK_ENGINE_VALIDATED
  EVIDENCE: Verified. Realistic account equity, ticks, OHLCV candles, and order lifecycle pass.

- [x] G5: Drop-in MetaTrader5 client API & AsyncMetaTrader5 client implementation
  CHECK: .venv/bin/pytest tests/test_client_api.py -v -s
  EXPECT: CLIENT_API_VALIDATED
  EVIDENCE: Verified. 1:1 drop-in functions, numpy array conversions, and pandas DataFrame conversions pass.

- [x] G6: Full test suite passes across all modules with zero failures
  CHECK: .venv/bin/pytest tests/ -v
  EXPECT: 25 passed
  EVIDENCE: Verified. 25/25 automated unit and integration tests passing in 0.73s.

- [x] G7: CLI management utility verification
  CHECK: .venv/bin/pytest tests/test_cli.py -v -s
  EXPECT: CLI_VALIDATED
  EVIDENCE: Verified. CLI status, mock server, and test-connect commands validated.

- [x] G8: Viral GitHub documentation, architecture diagrams, Dockerfile, and GitHub Actions CI
  CHECK: python3 scripts/verify_repo_readiness.py
  EXPECT: REPO_READINESS_VERIFIED
  EVIDENCE: Verified. Comprehensive README (9.7k chars), Dockerfile, CI/CD, and examples pass audit.

- [x] G9: Git repository initialized, commits recorded, and GitHub remote push attempted
  CHECK: git -C /home/rena/.gemini/antigravity/scratch/pymt5-linux status
  EXPECT: nothing to commit, working tree clean
  EVIDENCE: Verified. Git repo initialized, remote origin configured to git@github.com:renartacayle/pymt5-linux.git, ready to push once remote repo is created.
