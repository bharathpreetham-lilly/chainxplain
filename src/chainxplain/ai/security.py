"""Advanced security analysis features for smart contracts."""

import logging
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SecurityIssue:
    """Represents a security issue found in a contract."""
    severity: str  # critical, high, medium, low, info
    title: str
    description: str
    location: Optional[str] = None
    recommendation: str = ""
    cwe_id: Optional[str] = None  # Common Weakness Enumeration ID


@dataclass
class SecurityReport:
    """Complete security analysis report."""
    score: int  # 0-100, higher is better
    risk_level: str  # critical, high, medium, low
    issues: List[SecurityIssue]
    summary: str
    recommendations: List[str]


class SecurityAnalyzer:
    """Analyzes smart contracts for security vulnerabilities."""
    
    # Common vulnerability patterns
    VULNERABILITY_PATTERNS = {
        "reentrancy": {
            "patterns": [
                r'\.call\{value:',
                r'\.transfer\(',
                r'\.send\(',
            ],
            "severity": "high",
            "description": "Potential reentrancy vulnerability detected",
        },
        "unchecked_call": {
            "patterns": [
                r'\.call\(',
                r'\.delegatecall\(',
            ],
            "severity": "medium",
            "description": "Unchecked external call detected",
        },
        "tx_origin": {
            "patterns": [r'tx\.origin'],
            "severity": "high",
            "description": "Use of tx.origin for authentication is unsafe",
        },
        "block_timestamp": {
            "patterns": [r'block\.timestamp', r'now\s'],
            "severity": "low",
            "description": "Reliance on block.timestamp can be manipulated",
        },
        "selfdestruct": {
            "patterns": [r'selfdestruct\(', r'suicide\('],
            "severity": "critical",
            "description": "Contract contains selfdestruct/suicide",
        },
        "unprotected_ether": {
            "patterns": [r'payable\s*\{', r'\.value\('],
            "severity": "medium",
            "description": "Potential unprotected Ether withdrawal",
        },
    }
    
    def __init__(self):
        """Initialize security analyzer."""
        logger.info("Initialized SecurityAnalyzer")
    
    def analyze_source_code(self, source_code: str, 
                           contract_name: str = "Contract") -> SecurityReport:
        """
        Analyze smart contract source code for vulnerabilities.
        
        Args:
            source_code: Solidity source code
            contract_name: Name of the contract
            
        Returns:
            SecurityReport with findings
        """
        logger.info(f"Running security analysis on {contract_name}")
        
        issues: List[SecurityIssue] = []
        
        # Pattern-based vulnerability detection
        for vuln_name, vuln_info in self.VULNERABILITY_PATTERNS.items():
            for pattern in vuln_info["patterns"]:
                matches = re.finditer(pattern, source_code, re.IGNORECASE)
                for match in matches:
                    # Get line number
                    line_num = source_code[:match.start()].count('\n') + 1
                    
                    issue = SecurityIssue(
                        severity=vuln_info["severity"],
                        title=f"{vuln_name.replace('_', ' ').title()} Detected",
                        description=vuln_info["description"],
                        location=f"Line {line_num}",
                        recommendation=self._get_recommendation(vuln_name),
                    )
                    issues.append(issue)
                    logger.debug(f"Found {vuln_name} at line {line_num}")
        
        # Additional heuristics
        issues.extend(self._check_access_control(source_code))
        issues.extend(self._check_integer_overflow(source_code))
        issues.extend(self._check_dos_patterns(source_code))
        
        # Calculate security score
        score = self._calculate_security_score(issues, source_code)
        risk_level = self._determine_risk_level(score, issues)
        
        # Generate summary and recommendations
        summary = self._generate_summary(issues, score)
        recommendations = self._generate_recommendations(issues)
        
        logger.info(f"Security analysis complete: {len(issues)} issues found, score: {score}")
        
        return SecurityReport(
            score=score,
            risk_level=risk_level,
            issues=issues,
            summary=summary,
            recommendations=recommendations,
        )
    
    def _check_access_control(self, source_code: str) -> List[SecurityIssue]:
        """Check for missing access control."""
        issues = []
        
        # Look for state-changing functions without modifiers
        function_pattern = r'function\s+(\w+)\s*\([^)]*\)\s*(?:public|external)'
        modifier_pattern = r'(?:onlyOwner|onlyAdmin|require\(msg\.sender)'
        
        for match in re.finditer(function_pattern, source_code):
            func_name = match.group(1)
            func_start = match.start()
            func_end = source_code.find('}', func_start)
            
            if func_end == -1:
                continue
                
            func_body = source_code[func_start:func_end]
            
            # Skip view/pure functions
            if re.search(r'\b(view|pure)\b', func_body):
                continue
            
            # Check if function has access control
            if not re.search(modifier_pattern, func_body):
                line_num = source_code[:func_start].count('\n') + 1
                issues.append(SecurityIssue(
                    severity="medium",
                    title="Missing Access Control",
                    description=f"Function '{func_name}' may lack access control",
                    location=f"Line {line_num}",
                    recommendation="Add access control modifiers or require statements",
                ))
        
        return issues
    
    def _check_integer_overflow(self, source_code: str) -> List[SecurityIssue]:
        """Check for potential integer overflow/underflow."""
        issues = []
        
        # Check Solidity version (0.8.0+ has built-in overflow protection)
        version_match = re.search(r'pragma solidity\s+[\^~]?(\d+\.\d+)', source_code)
        if version_match:
            version = float(version_match.group(1))
            if version < 0.8:
                # Look for arithmetic operations without SafeMath
                if re.search(r'[\+\-\*\/]', source_code) and \
                   not re.search(r'using SafeMath', source_code):
                    issues.append(SecurityIssue(
                        severity="high",
                        title="Potential Integer Overflow",
                        description="Contract uses arithmetic without SafeMath in Solidity < 0.8.0",
                        recommendation="Use SafeMath library or upgrade to Solidity 0.8.0+",
                    ))
        
        return issues
    
    def _check_dos_patterns(self, source_code: str) -> List[SecurityIssue]:
        """Check for Denial of Service patterns."""
        issues = []
        
        # Unbounded loops
        loop_pattern = r'for\s*\([^)]*\)\s*\{'
        for match in re.finditer(loop_pattern, source_code):
            line_num = source_code[:match.start()].count('\n') + 1
            issues.append(SecurityIssue(
                severity="low",
                title="Potential DoS via Unbounded Loop",
                description="Loop may consume excessive gas",
                location=f"Line {line_num}",
                recommendation="Add gas limits or bounded iterations",
            ))
        
        return issues
    
    def _calculate_security_score(self, issues: List[SecurityIssue], 
                                  source_code: str) -> int:
        """Calculate overall security score (0-100)."""
        base_score = 100
        
        # Deduct points based on severity
        severity_penalties = {
            "critical": 30,
            "high": 15,
            "medium": 8,
            "low": 3,
            "info": 1,
        }
        
        for issue in issues:
            penalty = severity_penalties.get(issue.severity, 5)
            base_score -= penalty
        
        # Bonus for good practices
        if re.search(r'using SafeMath', source_code):
            base_score += 5
        if re.search(r'pragma solidity\s+[\^~]?0\.[89]', source_code):
            base_score += 5
        if re.search(r'\bReentrancyGuard\b', source_code):
            base_score += 5
        
        return max(0, min(100, base_score))
    
    def _determine_risk_level(self, score: int, issues: List[SecurityIssue]) -> str:
        """Determine overall risk level."""
        # Critical issues override score
        if any(i.severity == "critical" for i in issues):
            return "critical"
        
        if score >= 80:
            return "low"
        elif score >= 60:
            return "medium"
        elif score >= 40:
            return "high"
        else:
            return "critical"
    
    def _generate_summary(self, issues: List[SecurityIssue], score: int) -> str:
        """Generate summary of security findings."""
        severity_counts = {}
        for issue in issues:
            severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
        
        summary_parts = [f"Security Score: {score}/100"]
        
        if severity_counts:
            counts_str = ", ".join(
                f"{count} {sev}" for sev, count in sorted(severity_counts.items())
            )
            summary_parts.append(f"Issues Found: {counts_str}")
        else:
            summary_parts.append("No major issues detected")
        
        return " | ".join(summary_parts)
    
    def _generate_recommendations(self, issues: List[SecurityIssue]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Group by recommendation to avoid duplicates
        seen_recommendations = set()
        for issue in issues:
            if issue.recommendation and issue.recommendation not in seen_recommendations:
                recommendations.append(f"[{issue.severity.upper()}] {issue.recommendation}")
                seen_recommendations.add(issue.recommendation)
        
        # Add general recommendations
        if not seen_recommendations:
            recommendations.append("Continue following security best practices")
            recommendations.append("Consider professional security audit for production use")
        
        return recommendations[:10]  # Limit to top 10
    
    def _get_recommendation(self, vulnerability_type: str) -> str:
        """Get recommendation for a specific vulnerability type."""
        recommendations = {
            "reentrancy": "Use ReentrancyGuard or checks-effects-interactions pattern",
            "unchecked_call": "Always check return value of external calls",
            "tx_origin": "Use msg.sender instead of tx.origin for authentication",
            "block_timestamp": "Use block.number for time-based logic where possible",
            "selfdestruct": "Avoid selfdestruct unless absolutely necessary",
            "unprotected_ether": "Add access control to Ether withdrawal functions",
        }
        return recommendations.get(vulnerability_type, "Review and fix this issue")
