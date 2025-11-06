"""Export and reporting utilities for ChainXplain."""

import json
import logging
from typing import Any, Dict, Optional
from datetime import datetime
from pathlib import Path

from chainxplain.models import ContractAnalysis, WalletAnalysis, TransactionAnalysis

logger = logging.getLogger(__name__)


class ReportExporter:
    """Export analysis results to various formats."""
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize report exporter.
        
        Args:
            output_dir: Directory to save reports (default: ./reports)
        """
        self.output_dir = output_dir or Path("./reports")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"ReportExporter initialized with output dir: {self.output_dir}")
    
    def export_to_json(self, analysis: Any, filename: Optional[str] = None) -> Path:
        """
        Export analysis to JSON file.
        
        Args:
            analysis: ContractAnalysis, WalletAnalysis, or TransactionAnalysis
            filename: Output filename (auto-generated if not provided)
            
        Returns:
            Path to the exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            analysis_type = type(analysis).__name__.lower().replace("analysis", "")
            address_or_hash = getattr(analysis, 'address', None) or getattr(analysis, 'hash', 'unknown')
            filename = f"{analysis_type}_{address_or_hash[:10]}_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        # Convert Pydantic model to dict
        data = analysis.model_dump(mode='json')
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        logger.info(f"Exported JSON report to {filepath}")
        return filepath
    
    def export_to_markdown(self, analysis: Any, filename: Optional[str] = None) -> Path:
        """
        Export analysis to Markdown file.
        
        Args:
            analysis: ContractAnalysis, WalletAnalysis, or TransactionAnalysis
            filename: Output filename (auto-generated if not provided)
            
        Returns:
            Path to the exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            analysis_type = type(analysis).__name__.lower().replace("analysis", "")
            address_or_hash = getattr(analysis, 'address', None) or getattr(analysis, 'hash', 'unknown')
            filename = f"{analysis_type}_{address_or_hash[:10]}_{timestamp}.md"
        
        filepath = self.output_dir / filename
        
        if isinstance(analysis, ContractAnalysis):
            content = self._format_contract_markdown(analysis)
        elif isinstance(analysis, WalletAnalysis):
            content = self._format_wallet_markdown(analysis)
        elif isinstance(analysis, TransactionAnalysis):
            content = self._format_transaction_markdown(analysis)
        else:
            raise ValueError(f"Unsupported analysis type: {type(analysis)}")
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        logger.info(f"Exported Markdown report to {filepath}")
        return filepath
    
    def export_to_csv(self, analysis: Any, filename: Optional[str] = None) -> Path:
        """
        Export analysis to CSV file (key-value format).
        
        Args:
            analysis: ContractAnalysis, WalletAnalysis, or TransactionAnalysis
            filename: Output filename (auto-generated if not provided)
            
        Returns:
            Path to the exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            analysis_type = type(analysis).__name__.lower().replace("analysis", "")
            address_or_hash = getattr(analysis, 'address', None) or getattr(analysis, 'hash', 'unknown')
            filename = f"{analysis_type}_{address_or_hash[:10]}_{timestamp}.csv"
        
        filepath = self.output_dir / filename
        
        # Convert to dict
        data = analysis.model_dump(mode='json')
        
        # Flatten nested structures
        flat_data = self._flatten_dict(data)
        
        # Write CSV
        with open(filepath, 'w') as f:
            f.write("Field,Value\n")
            for key, value in flat_data.items():
                # Escape commas and quotes
                value_str = str(value).replace('"', '""')
                if ',' in value_str:
                    value_str = f'"{value_str}"'
                f.write(f"{key},{value_str}\n")
        
        logger.info(f"Exported CSV report to {filepath}")
        return filepath
    
    def _flatten_dict(self, data: Dict, parent_key: str = '', sep: str = '.') -> Dict:
        """Flatten a nested dictionary."""
        items = []
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                items.append((new_key, json.dumps(v)))
            else:
                items.append((new_key, v))
        return dict(items)
    
    def _format_contract_markdown(self, analysis: ContractAnalysis) -> str:
        """Format contract analysis as Markdown."""
        md = f"""# Contract Analysis Report

## Basic Information

- **Address**: `{analysis.address}`
- **Chain**: {analysis.chain}
- **Name**: {analysis.name or 'Unknown'}
- **Verified**: {'✅ Yes' if analysis.is_verified else '❌ No'}
- **Compiler Version**: {analysis.compiler_version or 'Unknown'}
- **Analysis Date**: {analysis.analyzed_at}

## AI Analysis

### Summary
{analysis.summary}

### Purpose
{analysis.purpose}

### Risk Assessment
- **Risk Level**: {analysis.risk_level.upper()}
- **Risk Factors**:
{self._format_list(analysis.risk_factors)}

### Key Functions
{self._format_list(analysis.key_functions)}

"""
        
        if analysis.token_info:
            md += f"""
## Token Information
{self._format_dict(analysis.token_info)}
"""
        
        if analysis.source_code and len(analysis.source_code) < 10000:
            md += f"""
## Source Code
```solidity
{analysis.source_code[:5000]}
{'...(truncated)' if len(analysis.source_code) > 5000 else ''}
```
"""
        
        return md
    
    def _format_wallet_markdown(self, analysis: WalletAnalysis) -> str:
        """Format wallet analysis as Markdown."""
        md = f"""# Wallet Analysis Report

## Basic Information

- **Address**: `{analysis.address}`
- **Chain**: {analysis.chain}
- **Native Balance**: {analysis.native_balance}
- **Total Transactions**: {analysis.total_transactions:,}
- **Analysis Date**: {analysis.analyzed_at}

## AI Analysis

### Summary
{analysis.summary}

### Activity Pattern
{analysis.activity_pattern}

### Wallet Type
{analysis.wallet_type}

### Notable Interactions
{self._format_list(analysis.notable_interactions)}

## Token Holdings

{self._format_dict(analysis.token_holdings) if analysis.token_holdings else 'No tokens held'}

## Recent Transactions

"""
        
        if analysis.recent_transactions:
            md += "| Hash | From | To | Value | Time |\n"
            md += "|------|------|----|----|------|\n"
            for tx in analysis.recent_transactions[:20]:
                md += f"| `{tx.hash[:10]}...` | `{tx.from_address[:8]}...` | `{tx.to_address[:8] if tx.to_address else 'N/A'}...` | {tx.value} | {tx.timestamp} |\n"
        else:
            md += "No recent transactions\n"
        
        return md
    
    def _format_transaction_markdown(self, analysis: TransactionAnalysis) -> str:
        """Format transaction analysis as Markdown."""
        md = f"""# Transaction Analysis Report

## Basic Information

- **Hash**: `{analysis.hash}`
- **Chain**: {analysis.chain}
- **Status**: {'✅ Success' if analysis.status else '❌ Failed'}
- **From**: `{analysis.from_address}`
- **To**: `{analysis.to_address or 'Contract Creation'}`
- **Value**: {analysis.value}
- **Gas Used**: {analysis.gas_used:,}
- **Gas Price**: {analysis.gas_price}
- **Timestamp**: {analysis.timestamp}
- **Analysis Date**: {analysis.analyzed_at}

## AI Explanation

{analysis.explanation}

### Method Called
{analysis.method_name or 'Unknown'}

### Parameters
{self._format_dict(analysis.parameters) if analysis.parameters else 'None'}

### Risks Detected
{self._format_list(analysis.risks_detected) if analysis.risks_detected else 'No risks detected'}

## Event Logs

Total events: {len(analysis.logs)}

"""
        
        if analysis.logs:
            md += "| Index | Topics | Data |\n"
            md += "|-------|--------|------|\n"
            for i, log in enumerate(analysis.logs[:10]):
                topics = log.get('topics', [])
                data = str(log.get('data', ''))[:20]
                md += f"| {i} | {len(topics)} topics | {data}... |\n"
            
            if len(analysis.logs) > 10:
                md += f"\n*...and {len(analysis.logs) - 10} more events*\n"
        
        return md
    
    def _format_list(self, items: list) -> str:
        """Format a list as Markdown bullet points."""
        if not items:
            return "- None\n"
        return "\n".join(f"- {item}" for item in items) + "\n"
    
    def _format_dict(self, data: dict) -> str:
        """Format a dictionary as Markdown."""
        if not data:
            return "None\n"
        return "\n".join(f"- **{k}**: {v}" for k, v in data.items()) + "\n"


def export_analysis(analysis: Any, format: str = "json", 
                   output_dir: Optional[Path] = None) -> Path:
    """
    Convenience function to export analysis.
    
    Args:
        analysis: Analysis object to export
        format: Export format (json, markdown, csv)
        output_dir: Output directory
        
    Returns:
        Path to exported file
    """
    exporter = ReportExporter(output_dir)
    
    if format == "json":
        return exporter.export_to_json(analysis)
    elif format == "markdown" or format == "md":
        return exporter.export_to_markdown(analysis)
    elif format == "csv":
        return exporter.export_to_csv(analysis)
    else:
        raise ValueError(f"Unsupported format: {format}. Use json, markdown, or csv")
