# Simulador de Mercado con Agentes IA Hiperrealistas

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Dependencies
- Verify Python 3.12+ is available: `python3 --version`
- Install project dependencies: `python3 -m pip install -r requirements.txt`
  - Takes ~5 minutes to complete. NEVER CANCEL. Set timeout to 10+ minutes.
  - Installs ML libraries (scikit-learn, pandas, matplotlib), web frameworks (FastAPI), database tools, and testing frameworks.

### Build and Run Commands
- Run main simulation: `python3 main.py`
  - Takes ~30 seconds for default 50-cycle simulation. NEVER CANCEL. Set timeout to 60+ minutes for longer simulations.
  - Generates comprehensive economic simulation with AI agents, banking systems, and market dynamics.
  - Creates outputs in `results/` directory: CSV data, PNG dashboards, JSON configs, and text reports.
- Run interactive examples: `echo "1" | python3 ejemplo_uso_completo.py`
  - Basic example (option 1) takes ~5 minutes. NEVER CANCEL. Set timeout to 10+ minutes.
  - Advanced and research examples may take longer depending on configuration.
  - Examples demonstrate AI agent system with neural networks, social networks, and coalition formation.

### Testing
- Run complete test suite: `./run_tests.sh`
  - Takes ~40 seconds total. NEVER CANCEL. Set timeout to 60+ minutes.
  - Includes unit tests (12 tests, ~1 second), integration tests (~1 second), and performance benchmarks.
  - Some tests may fail due to configuration issues but core functionality works correctly.
  - Test failures in performance tests are non-critical and don't affect main simulation.
- Run specific test categories:
  - Unit tests only: `python3 -m pytest tests/unit/ -v`
  - Integration tests only: `python3 -m pytest tests/integration/ -v`

## Validation

### Manual Validation Requirements
After making any changes, ALWAYS run through these validation scenarios:

#### Scenario 1: Basic Simulation Execution
1. Run `python3 main.py`
2. Wait for completion (~30 seconds)
3. Verify output shows: "SIMULACIÓN ECONÓMICA HIPERREALISTA v3.0 COMPLETADA EXITOSAMENTE"
4. Check that `results/` directory contains generated files:
   - Dashboard PNG file
   - CSV data file
   - JSON configuration file
   - Text report file

#### Scenario 2: Example Script Functionality
1. Run `echo "1" | python3 ejemplo_uso_completo.py`
2. Wait for completion (~5 minutes)
3. Verify AI agent system initializes with 15 consumers and 6 companies
4. Confirm 150 simulation cycles complete without critical errors
5. Check final statistics show active agents and coalitions formed

#### Scenario 3: Test Suite Execution
1. Run `./run_tests.sh`
2. Wait for completion (~40 seconds)
3. Verify basic model tests pass (12/12 tests)
4. Confirm main simulator execution test passes
5. Review test summary in `test_reports/test_summary.txt`

### Key Verification Points
- PIB (GDP) values should be realistic (typically $100,000 - $1,000,000 range)
- Inflation rates should be reasonable (-10% to +20%)
- No Python import errors or missing dependencies
- Log files contain detailed economic metrics and system status
- Generated dashboards display economic indicators visually

## Configuration and Customization

### Main Configuration File
- Edit `config_simulacion.json` to customize simulation parameters:
  - `simulacion.num_ciclos`: Number of simulation cycles (default: 50)
  - `simulacion.num_consumidores`: Number of consumer agents (default: 250)
  - `economia.pib_inicial`: Initial GDP value (default: 100000)
  - `agentes_ia.activar`: Enable/disable AI agent system (default: true)

### Important File Locations
- Main entry point: `main.py` (54KB, comprehensive simulation runner)
- Source code: `src/` directory with modular architecture:
  - `src/models/`: Core economic models (Bien, Consumidor, Empresa, Mercado)
  - `src/systems/`: Advanced systems (Banking, AI, Crisis management)
  - `src/ai/`: AI agent implementation with neural networks
  - `src/config/`: Configuration management
  - `src/utils/`: Logging and utilities
- Test suite: `tests/unit/` and `tests/integration/`
- Configuration: `config_simulacion.json` and `config_simulacion_fase2.json`

## Common Issues and Solutions

### Dependency Problems
- If `pip install` fails due to network restrictions, install packages individually
- PostgreSQL dependencies (`psycopg2-binary`) may require system packages but usually install successfully
- ML libraries are large (~500MB total) - ensure adequate disk space and network bandwidth

### Simulation Issues  
- If simulation hangs, check log files in project root (format: `simulacion_YYYYMMDD_HHMMSS.log`)
- Economic instability warnings are normal - the system includes crisis management
- Zero PIB values in early cycles may indicate initialization issues but usually self-correct

### Test Failures
- Integration test failures related to `ConsumidorIA` missing attributes are known issues
- Performance test failures with 'manufacturados' category are non-critical
- Core functionality works despite some test failures - focus on main simulation success

## Project Architecture

### Core Components
This is a sophisticated economic simulation system with:
- **Multi-agent AI system**: Neural networks, social networks, coalition formation
- **Advanced economic modeling**: Banking, central bank, labor market, price dynamics  
- **Crisis simulation**: Financial crisis detection and management
- **Machine learning integration**: Predictive models and adaptive behavior
- **Comprehensive analytics**: Real-time dashboards and detailed reporting

### Performance Characteristics
- Default simulation (50 cycles, 250 agents): ~30 seconds
- Extended simulation (100 cycles): ~1-2 minutes
- AI agent examples: ~5 minutes for full demonstration
- Memory usage: ~100-200MB typical
- Generates 500KB+ of output data per simulation

### Research Applications
The system supports research in:
- Computational economics and artificial markets
- Multi-agent AI coordination and competition
- Complex adaptive systems and emergence
- Social network analysis in economic contexts
- Machine learning applications in finance

## Development Guidelines

### Making Changes
- Always test changes with `python3 main.py` first
- Run relevant tests before committing: `./run_tests.sh`
- Check log files for detailed system behavior
- Validate output files are generated correctly in `results/`

### Code Structure
- Follow existing modular architecture in `src/`
- Economic models inherit from base classes in `src/models/`
- System integrations go in `src/systems/`
- AI components belong in `src/ai/`
- Configuration changes should update `config_simulacion.json`

### Debugging
- Enable detailed logging by setting `logs_detallados: true` in AI configuration
- Monitor system logs for economic alerts and warnings
- Use test reports in `test_reports/` for diagnostic information
- Check generated CSV files for data validation

Remember: This is a complex economic simulation system. NEVER CANCEL long-running operations - they are designed to complete comprehensive economic modeling that requires significant computation time.