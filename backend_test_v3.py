#!/usr/bin/env python3
"""
PerformOS One-on-One Builder V3 - Backend API Testing
Tests all V3 API endpoints including locked submissions and duplicate prevention
"""

import requests
import sys
import json
from datetime import datetime

class PerformOSV3APITester:
    def __init__(self, base_url="https://exact-port.preview.emergentagent.com"):
        self.base_url = base_url
        self.manager_token = None
        self.team_member_token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")
            self.failed_tests.append(f"{name}: {details}")

    def make_request(self, method, endpoint, token=None, data=None, expected_status=200):
        """Make API request with error handling"""
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = f'Bearer {token}'

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PATCH':
                response = requests.patch(url, json=data, headers=headers, timeout=10)
            else:
                return False, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            if success:
                try:
                    return True, response.json()
                except:
                    return True, {}
            else:
                return False, f"Status {response.status_code}: {response.text[:200]}"
        except Exception as e:
            return False, str(e)

    def test_connectivity(self):
        """Test basic API connectivity"""
        success, result = self.make_request('GET', '/')
        if success and isinstance(result, dict):
            self.log_test("Backend API connectivity", True)
            return True
        else:
            self.log_test("Backend API connectivity", False, result)
            return False

    def test_manager_login(self):
        """Test manager login"""
        success, result = self.make_request(
            'POST', 
            '/api/auth/login',
            data={"email": "alex@performos.io", "password": "demo"}
        )
        
        if success and isinstance(result, dict) and 'access_token' in result:
            self.manager_token = result['access_token']
            user = result.get('user', {})
            if user.get('role') == 'manager':
                self.log_test("Manager login (alex@performos.io)", True)
                return True
            else:
                self.log_test("Manager login", False, f"Expected manager role, got: {user.get('role')}")
                return False
        else:
            self.log_test("Manager login", False, result)
            return False

    def test_team_member_login(self):
        """Test team member login"""
        success, result = self.make_request(
            'POST', 
            '/api/auth/login',
            data={"email": "sarah@performos.io", "password": "demo"}
        )
        
        if success and isinstance(result, dict) and 'access_token' in result:
            self.team_member_token = result['access_token']
            user = result.get('user', {})
            if user.get('role') == 'team_member':
                self.log_test("Team member login (sarah@performos.io)", True)
                return True
            else:
                self.log_test("Team member login", False, f"Expected team_member role, got: {user.get('role')}")
                return False
        else:
            self.log_test("Team member login", False, result)
            return False

    def test_weekly_schedule(self):
        """Test weekly schedule endpoint"""
        success, result = self.make_request('GET', '/api/schedule/weeks')
        
        if success and isinstance(result, dict):
            weeks = result.get('weeks', [])
            current_week = result.get('current_week')
            if len(weeks) >= 15 and current_week == "2026-03-23":
                self.log_test(f"Weekly schedule ({len(weeks)} Monday dates, current: {current_week})", True)
                return True
            else:
                self.log_test("Weekly schedule", False, f"Expected >=15 weeks with current week 2026-03-23, got {len(weeks)} weeks, current: {current_week}")
                return False
        else:
            self.log_test("Weekly schedule", False, f"Expected dict, got: {type(result)}")
            return False

    def test_schedule_status(self):
        """Test schedule status for team member"""
        success, result = self.make_request('GET', '/api/schedule/status', token=self.team_member_token)
        
        if success and isinstance(result, list) and len(result) >= 15:
            current_week_status = next((s for s in result if s.get('is_current_week')), None)
            if current_week_status and current_week_status.get('date') == "2026-03-23":
                submitted_count = sum(1 for s in result if s.get('submitted'))
                self.log_test(f"Schedule status ({len(result)} weeks, {submitted_count} submitted)", True)
                return True
            else:
                self.log_test("Schedule status", False, "No current week (2026-03-23) found in status")
                return False
        else:
            self.log_test("Schedule status", False, f"Expected list of >=15 items, got: {type(result)} {len(result) if isinstance(result, list) else 'non-list'}")
            return False

    def test_manager_dashboard_stats(self):
        """Test manager dashboard stats"""
        success, result = self.make_request('GET', '/api/stats/dashboard', token=self.manager_token)
        
        expected_keys = ['this_week_submissions', 'total_team_members', 'team_health_score', 'active_flags']
        if success and isinstance(result, dict):
            missing_keys = [key for key in expected_keys if key not in result]
            if not missing_keys:
                stats = f"Submissions: {result.get('this_week_submissions')}/{result.get('total_team_members')}, Health: {result.get('team_health_score')}%, Flags: {result.get('active_flags')}"
                self.log_test(f"Manager dashboard stats ({stats})", True)
                return True
            else:
                self.log_test("Manager dashboard stats", False, f"Missing keys: {missing_keys}")
                return False
        else:
            self.log_test("Manager dashboard stats", False, f"Expected dict, got: {type(result)}")
            return False

    def test_manager_members(self):
        """Test manager members list"""
        success, result = self.make_request('GET', '/api/members', token=self.manager_token)
        
        if success and isinstance(result, list) and len(result) == 6:
            member_names = [m.get('name', 'Unknown') for m in result]
            self.log_test(f"Manager members list (6 team members: {', '.join(member_names[:3])}...)", True)
            return True
        else:
            self.log_test("Manager members list", False, f"Expected 6 members, got: {type(result)} {len(result) if isinstance(result, list) else 'non-list'}")
            return False

    def test_manager_flags(self):
        """Test manager flags list"""
        success, result = self.make_request('GET', '/api/flags?status_filter=open', token=self.manager_token)
        
        if success and isinstance(result, list):
            flag_count = len(result)
            severities = {}
            for flag in result:
                severity = flag.get('severity', 'unknown')
                severities[severity] = severities.get(severity, 0) + 1
            
            severity_str = ', '.join([f"{k}: {v}" for k, v in severities.items()])
            self.log_test(f"Manager flags list ({flag_count} active flags - {severity_str})", True)
            return True
        else:
            self.log_test("Manager flags list", False, f"Expected list, got: {type(result)}")
            return False

    def test_submissions_list(self):
        """Test submissions endpoint for manager"""
        success, result = self.make_request('GET', '/api/submissions', token=self.manager_token)
        
        if success and isinstance(result, list):
            locked_count = sum(1 for s in result if s.get('locked'))
            self.log_test(f"Manager submissions list ({len(result)} total, {locked_count} locked)", True)
            return True
        else:
            self.log_test("Manager submissions list", False, f"Expected list, got: {type(result)}")
            return False

    def test_team_member_submissions(self):
        """Test team member submissions list"""
        success, result = self.make_request('GET', '/api/submissions', token=self.team_member_token)
        
        if success and isinstance(result, list):
            locked_count = sum(1 for s in result if s.get('locked'))
            self.log_test(f"Team member submissions list ({len(result)} submissions, {locked_count} locked)", True)
            return True
        else:
            self.log_test("Team member submissions list", False, result)
            return False

    def test_locked_submission_prevention(self):
        """Test that locked submissions cannot be resubmitted"""
        # First, get a locked submission date
        success, submissions = self.make_request('GET', '/api/submissions', token=self.team_member_token)
        
        if not success or not isinstance(submissions, list):
            self.log_test("Locked submission prevention", False, "Could not get submissions list")
            return False
        
        locked_submission = next((s for s in submissions if s.get('locked')), None)
        if not locked_submission:
            self.log_test("Locked submission prevention", False, "No locked submissions found to test")
            return False
        
        # Try to submit to the same date
        test_data = {
            "member_id": "placeholder",
            "date": locked_submission['date'],
            "responses": {
                "proud_of": {"rating": 4, "comment": "Test submission"},
                "stuck_on": {"rating": 2, "comment": "Test comment"},
                "need_from_manager": {"rating": 3, "comment": "Test comment"},
                "target_confidence": {"rating": 4, "comment": "Test comment"},
                "feeling_about_work": {"rating": 4, "comment": "Test comment"},
                "safe_to_raise_concerns": {"rating": 5, "comment": "Test comment"},
                "feel_supported": {"rating": 4, "comment": "Test comment"},
                "workload_manageable": {"rating": 4, "comment": "Test comment"}
            }
        }
        
        success, result = self.make_request(
            'POST', 
            '/api/submissions', 
            token=self.team_member_token,
            data=test_data,
            expected_status=400
        )
        
        if success:
            self.log_test(f"Locked submission prevention (date: {locked_submission['date']})", True)
            return True
        else:
            self.log_test("Locked submission prevention", False, f"Should have prevented resubmission: {result}")
            return False

    def test_new_submission_locking(self):
        """Test that new submissions are immediately locked"""
        # Find an open week to submit to
        success, status_list = self.make_request('GET', '/api/schedule/status', token=self.team_member_token)
        
        if not success or not isinstance(status_list, list):
            self.log_test("New submission locking", False, "Could not get schedule status")
            return False
        
        open_week = next((s for s in status_list if not s.get('submitted')), None)
        if not open_week:
            self.log_test("New submission locking", False, "No open weeks found to test submission")
            return False
        
        # Submit to the open week
        test_data = {
            "member_id": "placeholder",
            "date": open_week['date'],
            "responses": {
                "proud_of": {"rating": 4, "comment": "Test submission for locking"},
                "stuck_on": {"rating": 2, "comment": "Test comment"},
                "need_from_manager": {"rating": 3, "comment": "Test comment"},
                "target_confidence": {"rating": 4, "comment": "Test comment"},
                "feeling_about_work": {"rating": 4, "comment": "Test comment"},
                "safe_to_raise_concerns": {"rating": 5, "comment": "Test comment"},
                "feel_supported": {"rating": 4, "comment": "Test comment"},
                "workload_manageable": {"rating": 4, "comment": "Test comment"}
            }
        }
        
        success, result = self.make_request(
            'POST', 
            '/api/submissions', 
            token=self.team_member_token,
            data=test_data,
            expected_status=200
        )
        
        if success and isinstance(result, dict) and result.get('locked'):
            self.log_test(f"New submission locking (date: {open_week['date']}, locked: {result.get('locked')[:19]})", True)
            return True
        else:
            self.log_test("New submission locking", False, f"Submission should be immediately locked: {result}")
            return False

    def test_submission_validation(self):
        """Test submission validation for required fields"""
        # Find an open week
        success, status_list = self.make_request('GET', '/api/schedule/status', token=self.team_member_token)
        
        if not success or not isinstance(status_list, list):
            self.log_test("Submission validation", False, "Could not get schedule status")
            return False
        
        open_week = next((s for s in status_list if not s.get('submitted')), None)
        if not open_week:
            # Use a future date for testing
            test_date = "2026-06-29"
        else:
            test_date = open_week['date']
        
        # Submit incomplete data (missing required fields)
        incomplete_data = {
            "member_id": "placeholder",
            "date": test_date,
            "responses": {
                "proud_of": {"rating": 4, "comment": "Test submission"},
                # Missing other required fields
            }
        }
        
        success, result = self.make_request(
            'POST', 
            '/api/submissions', 
            token=self.team_member_token,
            data=incomplete_data,
            expected_status=400
        )
        
        if success:
            self.log_test("Submission validation (incomplete data rejected)", True)
            return True
        else:
            self.log_test("Submission validation", False, f"Should have rejected incomplete submission: {result}")
            return False

    def run_all_tests(self):
        """Run all API tests"""
        print("🧪 Starting PerformOS One-on-One Builder V3 API Tests")
        print("🌐 Testing against:", self.base_url)
        print("=" * 70)
        
        # Test sequence
        tests = [
            self.test_connectivity,
            self.test_manager_login,
            self.test_team_member_login,
            self.test_weekly_schedule,
            self.test_schedule_status,
            self.test_manager_dashboard_stats,
            self.test_manager_members,
            self.test_manager_flags,
            self.test_submissions_list,
            self.test_team_member_submissions,
            self.test_locked_submission_prevention,
            self.test_new_submission_locking,
            self.test_submission_validation,
        ]
        
        # Run all tests
        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"❌ Test {test.__name__} failed with exception: {str(e)}")
                self.failed_tests.append(f"{test.__name__}: {str(e)}")
        
        # Print results
        print("\n" + "=" * 70)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        
        if self.failed_tests:
            print("\n❌ Failed Tests:")
            for failure in self.failed_tests:
                print(f"   • {failure}")
        else:
            print("\n✅ All tests passed!")
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"\n🎯 Success Rate: {success_rate:.1f}%")
        
        return self.tests_passed == self.tests_run

def main():
    tester = PerformOSV3APITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())