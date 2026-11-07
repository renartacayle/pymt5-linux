# Gates: pymt5-linux

OWNS: pyproject.toml, src/**, tests/**, examples/**, scripts/**, .github/**, README.md, LICENSE, Dockerfile

Scope: Production-grade MetaTrader 5 SDK and drop-in replacement for Linux with Wine IPC bridge, remote gateway, mock simulator, and async streaming support.

- [ ] G1: Package structure and pyproject.toml configuration validated
  CHECK: .venv/bin/pytest tests/test_package.py -k test_package_metadata -v
  EXPECT: test_package_metadata PASSED
  EVIDENCE: pending

- [ ] G2: Complete MT5 constants, enums, data structures, and namedtuples specification
  CHECK: .venv/bin/pytest tests/test_constants_and_types.py -v -s
  EXPECT: ALL_TYPES_VALIDATED
  EVIDENCE: pending

- [ ] G3: Protocol serialization, packet framing, and network transport
  CHECK: .venv/bin/pytest tests/test_protocol.py -v -s
  EXPECT: PROTOCOL_VALIDATED
  EVIDENCE: pending

- [ ] G4: Standalone Wine gateway and mock trading simulator engine
  CHECK: .venv/bin/pytest tests/test_mock_engine.py -v -s
  EXPECT: MOCK_ENGINE_VALIDATED
  EVIDENCE: pending

- [ ] G5: Drop-in MetaTrader5 client API & AsyncMetaTrader5 client implementation
  CHECK: .venv/bin/pytest tests/test_client_api.py -v -s
  EXPECT: CLIENT_API_VALIDATED
  EVIDENCE: pending

- [ ] G6: Full test suite passes across all modules with zero failures
  CHECK: .venv/bin/pytest tests/ -v
  EXPECT: 25 passed
  EVIDENCE: pending

- [ ] G7: CLI management utility verification
  CHECK: .venv/bin/pytest tests/test_cli.py -v -s
  EXPECT: CLI_VALIDATED
  EVIDENCE: pending

- [ ] G8: Viral GitHub documentation, architecture diagrams, Dockerfile, and GitHub Actions CI
  CHECK: python3 scripts/verify_repo_readiness.py
  EXPECT: REPO_READINESS_VERIFIED
  EVIDENCE: pending

- [ ] G9: Git repository initialized, commits recorded, and GitHub remote push attempted
  CHECK: git -C /home/rena/.gemini/antigravity/scratch/pymt5-linux status
  EXPECT: nothing to commit, working tree clean
  EVIDENCE: pending
