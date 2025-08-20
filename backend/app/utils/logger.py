"""
Logging configuration for the Autonomous Research & Report Generation System
"""

import logging
import logging.config
import sys
from typing import Dict, Any
import json
from datetime import datetime
from pathlib import Path

from app.core.config import settings


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add extra fields if present
        if hasattr(record, 'method'):
            log_entry['method'] = record.method
        if hasattr(record, 'path'):
            log_entry['path'] = record.path
        if hasattr(record, 'status_code'):
            log_entry['status_code'] = record.status_code
        if hasattr(record, 'process_time'):
            log_entry['process_time'] = record.process_time
        if hasattr(record, 'client_ip'):
            log_entry['client_ip'] = record.client_ip
        if hasattr(record, 'user_agent'):
            log_entry['user_agent'] = record.user_agent
        if hasattr(record, 'job_id'):
            log_entry['job_id'] = record.job_id
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': self.formatException(record.exc_info)
            }
        
        return json.dumps(log_entry)


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors"""
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Format the message
        formatted = super().format(record)
        
        # Add color to level name
        formatted = formatted.replace(
            record.levelname,
            f"{color}{record.levelname}{reset}"
        )
        
        return formatted


def setup_logging() -> None:
    """Setup logging configuration"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Define logging configuration
    logging_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": JSONFormatter,
            },
            "colored": {
                "()": ColoredFormatter,
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.LOG_LEVEL,
                "formatter": "colored" if settings.ENVIRONMENT == "development" else "json",
                "stream": sys.stdout,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "json",
                "filename": log_dir / "app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "json",
                "filename": log_dir / "error.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
        },
        "loggers": {
            "": {  # Root logger
                "level": settings.LOG_LEVEL,
                "handlers": ["console", "file", "error_file"],
                "propagate": False,
            },
            "app": {  # Application logger
                "level": settings.LOG_LEVEL,
                "handlers": ["console", "file", "error_file"],
                "propagate": False,
            },
            "uvicorn": {  # Uvicorn logger
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "uvicorn.access": {  # Uvicorn access logger
                "level": "INFO",
                "handlers": ["file"],
                "propagate": False,
            },
            "sqlalchemy": {  # SQLAlchemy logger
                "level": "WARNING",
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "celery": {  # Celery logger
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "langchain": {  # LangChain logger
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "langgraph": {  # LangGraph logger
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False,
            },
        },
    }
    
    # Apply logging configuration
    logging.config.dictConfig(logging_config)
    
    # Set specific loggers
    logging.getLogger("app").setLevel(settings.LOG_LEVEL)
    
    # Suppress noisy loggers in production
    if settings.ENVIRONMENT == "production":
        logging.getLogger("uvicorn.access").setLevel("WARNING")
        logging.getLogger("sqlalchemy.engine").setLevel("WARNING")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name"""
    return logging.getLogger(f"app.{name}")


# Convenience functions for common logging patterns
def log_request(logger: logging.Logger, method: str, path: str, status_code: int, 
                process_time: float, client_ip: str = None, user_agent: str = None) -> None:
    """Log HTTP request details"""
    logger.info(
        f"Request: {method} {path} - {status_code} ({process_time:.3f}s)",
        extra={
            "method": method,
            "path": path,
            "status_code": status_code,
            "process_time": process_time,
            "client_ip": client_ip,
            "user_agent": user_agent,
        }
    )


def log_job_event(logger: logging.Logger, event: str, job_id: str, user_id: str = None, 
                  details: Dict[str, Any] = None) -> None:
    """Log research job events"""
    logger.info(
        f"Job Event: {event} - Job ID: {job_id}",
        extra={
            "event": event,
            "job_id": job_id,
            "user_id": user_id,
            "details": details,
        }
    )


def log_error(logger: logging.Logger, error: Exception, context: Dict[str, Any] = None) -> None:
    """Log errors with context"""
    logger.error(
        f"Error: {str(error)}",
        extra={
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
        },
        exc_info=True
    )


def log_performance(logger: logging.Logger, operation: str, duration: float, 
                   details: Dict[str, Any] = None) -> None:
    """Log performance metrics"""
    logger.info(
        f"Performance: {operation} - {duration:.3f}s",
        extra={
            "operation": operation,
            "duration": duration,
            "details": details,
        }
    )
