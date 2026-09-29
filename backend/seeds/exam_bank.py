"""Original practice items aligned to publicly published exam domains.

These are not official AWS, CompTIA, or PMI questions and are not copied
from vendor exams or dumps. Each item tests a concept from that exam's
public guide / content outline.
"""

from datetime import datetime, timezone

from models import Exam, Question, QuestionChoice, Topic

SOURCE_TYPE = "generated"
SOURCE_NAME = "Original PrepPilot item aligned to public exam domains"
LICENSE = "Original practice content; not an official exam question"

AWS_GUIDE = "https://aws.amazon.com/certification/certified-solutions-architect-associate/"
SECURITY_PLUS_GUIDE = "https://www.comptia.org/certifications/security"
PMP_GUIDE = "https://www.pmi.org/certifications/project-management-pmp"

BANK = [
    {
        "name": "AWS Solutions Architect Associate",
        "provider": "Amazon Web Services",
        "description": (
            "Original practice items mapped to SAA-C03 public domains: "
            "secure, resilient, high-performing, and cost-optimized architectures."
        ),
        "source_url": AWS_GUIDE,
        "topics": {
            "Storage": {
                "description": "Object, block, and shared file storage on AWS",
                "questions": [
                    {
                        "question_text": "Which AWS service is primarily used for object storage?",
                        "difficulty": "easy",
                        "explanation": (
                            "Amazon S3 stores objects (files plus metadata) and is the default "
                            "choice for durable object storage. EC2 is compute, RDS is managed "
                            "relational databases, and EBS is block storage attached to an instance."
                        ),
                        "choices": [
                            {"choice_text": "Amazon S3", "is_correct": True},
                            {"choice_text": "Amazon EC2", "is_correct": False},
                            {"choice_text": "Amazon RDS", "is_correct": False},
                            {"choice_text": "Amazon EBS", "is_correct": False},
                        ],
                    },
                    {
                        "question_text": (
                            "A fleet of Linux EC2 instances in one Region must mount the same "
                            "POSIX file system at the same time. Which service should you choose?"
                        ),
                        "difficulty": "medium",
                        "explanation": (
                            "Amazon EFS is an NFS file system that many Linux instances can mount "
                            "concurrently. EBS volumes are typically attached to one instance. "
                            "S3 is object storage, not a POSIX file system. Instance store is "
                            "ephemeral local disk on a single host."
                        ),
                        "choices": [
                            {"choice_text": "Amazon EFS", "is_correct": True},
                            {"choice_text": "A single Amazon EBS volume shared by IP address", "is_correct": False},
                            {"choice_text": "Amazon S3 Standard", "is_correct": False},
                            {"choice_text": "EC2 instance store", "is_correct": False},
                        ],
                    },
                ],
            },
            "Networking": {
                "description": "VPC connectivity, egress, and private routing",
                "questions": [
                    {
                        "question_text": (
                            "EC2 instances in a private subnet need outbound internet access for "
                            "patches, but must not be reachable from the public internet. "
                            "What should you use?"
                        ),
                        "difficulty": "medium",
                        "explanation": (
                            "A NAT gateway in a public subnet lets private instances initiate "
                            "outbound connections without having public IPs. An internet gateway "
                            "on the private subnet (or public IPs on those instances) would expose "
                            "them. VPC peering and security-group inbound 0.0.0.0/0 do not provide "
                            "controlled egress for this design."
                        ),
                        "choices": [
                            {"choice_text": "A NAT gateway in a public subnet", "is_correct": True},
                            {
                                "choice_text": "An internet gateway attached only to the private subnet",
                                "is_correct": False,
                            },
                            {"choice_text": "VPC peering to another private VPC", "is_correct": False},
                            {
                                "choice_text": "A security group that allows inbound 0.0.0.0/0",
                                "is_correct": False,
                            },
                        ],
                    },
                    {
                        "question_text": (
                            "Two VPCs in the same Region need to communicate using private IP "
                            "addresses. There is no overlapping CIDR. What is the simplest fit?"
                        ),
                        "difficulty": "easy",
                        "explanation": (
                            "VPC peering connects two VPCs so traffic stays on the AWS private "
                            "network using private IPs. A site-to-site VPN is for on-premises "
                            "connectivity. An internet gateway provides public internet paths. "
                            "CloudFront is a CDN, not VPC-to-VPC routing."
                        ),
                        "choices": [
                            {"choice_text": "VPC peering", "is_correct": True},
                            {"choice_text": "AWS Site-to-Site VPN to the public internet only", "is_correct": False},
                            {"choice_text": "An internet gateway on both VPCs", "is_correct": False},
                            {"choice_text": "Amazon CloudFront", "is_correct": False},
                        ],
                    },
                ],
            },
            "Secure Architectures": {
                "description": "SAA-C03 Domain 1: identity, access, and encryption",
                "questions": [
                    {
                        "question_text": (
                            "An application on EC2 must read objects from one S3 bucket. You want "
                            "to avoid storing long-term access keys on the instance. What should you do?"
                        ),
                        "difficulty": "easy",
                        "explanation": (
                            "An IAM role attached via an instance profile provides temporary "
                            "credentials through the instance metadata service. Embedding access "
                            "keys, using the root user, or making the bucket public all violate "
                            "least privilege and common SAA security guidance."
                        ),
                        "choices": [
                            {"choice_text": "Attach an IAM role to the instance", "is_correct": True},
                            {
                                "choice_text": "Save IAM user access keys in a file on the instance",
                                "is_correct": False,
                            },
                            {"choice_text": "Use the AWS account root user from the instance", "is_correct": False},
                            {"choice_text": "Make the bucket publicly readable", "is_correct": False},
                        ],
                    },
                    {
                        "question_text": (
                            "A team wants S3 objects encrypted at rest with auditability of which "
                            "customer-managed key was used. Which encryption option fits best?"
                        ),
                        "difficulty": "medium",
                        "explanation": (
                            "SSE-KMS uses AWS KMS keys, which you can manage, restrict, and audit "
                            "via CloudTrail. SSE-S3 uses AWS-managed S3 keys with less customer "
                            "key control. Turning encryption off fails the requirement. Forcing "
                            "only client-side encryption is possible but is not required when "
                            "SSE-KMS meets the need."
                        ),
                        "choices": [
                            {"choice_text": "SSE-KMS with a customer managed key", "is_correct": True},
                            {"choice_text": "Disable server-side encryption", "is_correct": False},
                            {
                                "choice_text": "SSE-S3 only, with no KMS key policy controls",
                                "is_correct": False,
                            },
                            {
                                "choice_text": "Store objects unencrypted and rely on HTTPS alone",
                                "is_correct": False,
                            },
                        ],
                    },
                ],
            },
            "Resilient Architectures": {
                "description": "SAA-C03 Domain 2: high availability and scaling",
                "questions": [
                    {
                        "question_text": (
                            "A production PostgreSQL database must survive the loss of one "
                            "Availability Zone with automatic failover and the same endpoint. "
                            "Which design should you use?"
                        ),
                        "difficulty": "medium",
                        "explanation": (
                            "RDS Multi-AZ keeps a synchronous standby in another AZ and fails "
                            "over automatically using the same DNS endpoint. A single-AZ instance "
                            "plus snapshots requires a restore and downtime. ElastiCache is not "
                            "your primary relational database. S3 is object storage."
                        ),
                        "choices": [
                            {"choice_text": "Amazon RDS Multi-AZ", "is_correct": True},
                            {
                                "choice_text": "Single-AZ RDS plus a daily snapshot only",
                                "is_correct": False,
                            },
                            {"choice_text": "Amazon ElastiCache for Redis as the system of record", "is_correct": False},
                            {"choice_text": "Store database files only in Amazon S3", "is_correct": False},
                        ],
                    },
                    {
                        "question_text": (
                            "A public web application should add and remove EC2 instances as CPU "
                            "changes, and users should hit one HTTPS entry point. What do you combine?"
                        ),
                        "difficulty": "medium",
                        "explanation": (
                            "An Application Load Balancer distributes HTTPS traffic across an "
                            "Auto Scaling group that grows and shrinks with demand. A single "
                            "large instance does not scale out. Route 53 alone does not replace "
                            "an instance fleet. SQS is a queue, not a user-facing HTTPS front door."
                        ),
                        "choices": [
                            {
                                "choice_text": "Application Load Balancer and an Auto Scaling group",
                                "is_correct": True,
                            },
                            {"choice_text": "One extra-large EC2 instance", "is_correct": False},
                            {"choice_text": "Amazon Route 53 with no load balancer or scaling", "is_correct": False},
                            {"choice_text": "Amazon SQS as the only public endpoint", "is_correct": False},
                        ],
                    },
                ],
            },
            "Cost Optimization": {
                "description": "SAA-C03 Domain 4: storage classes and data transfer cost",
                "questions": [
                    {
                        "question_text": (
                            "Archive objects are read about once a quarter. Retrieval in 1–5 "
                            "minutes is acceptable. You want the lowest storage cost among "
                            "common S3 classes. Which class fits?"
                        ),
                        "difficulty": "medium",
                        "explanation": (
                            "S3 Glacier Flexible Retrieval is built for infrequent archives with "
                            "retrieval typically in minutes. S3 Standard and Standard-IA cost "
                            "more to store for this access pattern. EBS gp3 is block storage "
                            "for instances, not an archive object class."
                        ),
                        "choices": [
                            {"choice_text": "S3 Glacier Flexible Retrieval", "is_correct": True},
                            {"choice_text": "S3 Standard", "is_correct": False},
                            {"choice_text": "S3 Standard-IA", "is_correct": False},
                            {"choice_text": "Amazon EBS gp3 volumes", "is_correct": False},
                        ],
                    },
                    {
                        "question_text": (
                            "The same static assets are downloaded by users worldwide. You want "
                            "to cut origin data-transfer cost and latency. What should you add?"
                        ),
                        "difficulty": "easy",
                        "explanation": (
                            "CloudFront caches copies at edge locations so most downloads never "
                            "hit the S3 origin. Copying buckets into every Region by hand is "
                            "operationally heavy. A NAT gateway is for private-subnet egress. "
                            "Direct Connect is a private network to AWS, not a global CDN."
                        ),
                        "choices": [
                            {"choice_text": "Amazon CloudFront in front of Amazon S3", "is_correct": True},
                            {
                                "choice_text": "Manually copy the bucket into every AWS Region",
                                "is_correct": False,
                            },
                            {"choice_text": "A NAT gateway in each public subnet", "is_correct": False},
                            {"choice_text": "AWS Direct Connect only", "is_correct": False},
                        ],
                    },
                ],
            },
        },
    },
    {
        "name": "CompTIA Security+",
        "provider": "CompTIA",
        "description": (
            "Original practice items mapped to SY0-701 public domains: general concepts, "
            "threats, architecture, operations, and program management."
        ),
        "source_url": SECURITY_PLUS_GUIDE,
        "topics": {
            "General Security Concepts": {
                "description": "SY0-701 Domain 1: CIA, identity, and foundational controls",
                "questions": [
                    {
                        "question_text": (
                            "A company encrypts laptop disks so stolen hardware does not expose "
                            "customer files. Which CIA triad goal is this control mainly protecting?"
                        ),
                        "difficulty": "easy",
                        "explanation": (
                            "Encryption of data at rest protects confidentiality: unauthorized "
                            "people should not read the data. Integrity is about detecting or "
                            "preventing unauthorized change. Availability is about systems staying "
                            "usable. Non-repudiation is about proving who performed an action."
                        ),
                        "choices": [
                            {"choice_text": "Confidentiality", "is_correct": True},
                            {"choice_text": "Integrity", "is_correct": False},
                            {"choice_text": "Availability", "is_correct": False},
                            {"choice_text": "Non-repudiation", "is_correct": False},
                        ],
                    },
                    {
                        "question_text": (
                            "Which example is multi-factor authentication rather than multiple "
                            "examples of the same factor?"
                        ),
                        "difficulty": "easy",
                        "explanation": (
                            "MFA combines different factor types, such as something you know "
                            "(password) and something you have (authenticator app). Two passwords "
                            "or a password plus a security question are still knowledge factors. "
                            "A longer password is still a single factor."
                        ),
                        "choices": [
                            {
                                "choice_text": "Account password plus a rotating authenticator-app code",
                                "is_correct": True,
                            },
                            {"choice_text": "A password and a second, different password", "is_correct": False},
                            {"choice_text": "A 24-character password by itself", "is_correct": False},
                            {"choice_text": "A password plus the name of your first pet", "is_correct": False},
                        ],
                    },
                ],
            },
            "Threats and Vulnerabilities": {
                "description": "SY0-701 Domain 2: social engineering and common attacks",
                "questions": [
                    {
                        "question_text": (
                            "Employees receive an email that looks like it came from IT and asks "
                            "them to click a link and enter their password. What is this?"
                        ),
                        "difficulty": "easy",
                        "explanation": (
                            "Phishing uses deceptive messages to steal credentials or deliver "
                            "malware. Tailgating is following someone through a physical door. "
                            "Dumpster diving is searching discarded papers. A replay attack "
                            "reuses a captured valid authentication sequence."
                        ),
                        "choices": [
                            {"choice_text": "Phishing", "is_correct": True},
                            {"choice_text": "Tailgating", "is_correct": False},
                            {"choice_text": "Dumpster diving", "is_correct": False},
                            {"choice_text": "A replay attack", "is_correct": False},
                        ],
                    },
                    {
                        "question_text": (
                            "An attacker calls the help desk, claims to be a vendor technician, "
                            "and talks the agent into resetting a privileged password. Which "
                            "social-engineering tactic is this?"
                        ),
                        "difficulty": "medium",
                        "explanation": (
                            "Pretexting is inventing a believable story and identity to get "
                            "someone to break procedure. XSS and SQL injection are technical "
                            "application attacks. A rainbow table is a password-cracking aid, "
                            "not a phone conversation."
                        ),
                        "choices": [
                            {"choice_text": "Pretexting", "is_correct": True},
                            {"choice_text": "Cross-site scripting (XSS)", "is_correct": False},
                            {"choice_text": "SQL injection", "is_correct": False},
                            {"choice_text": "Rainbow-table attack", "is_correct": False},
                        ],
                    },
                ],
            },
            "Security Architecture": {
                "description": "SY0-701 Domain 3: models, trust, and integrity controls",
                "questions": [
                    {
                        "question_text": (
                            "A design assumes no user or device is trusted just because it is "
                            "inside the corporate network. Every request must be authenticated "
                            "and authorized. What model is this?"
                        ),
                        "difficulty": "medium",
                        "explanation": (
                            "Zero trust removes implicit trust based on network location. "
                            "Castle-and-moat (perimeter-only) trust is the older opposite idea. "
                            "MAC flooding and war driving are attacks, not architecture models."
                        ),
                        "choices": [
                            {"choice_text": "Zero trust", "is_correct": True},
                            {"choice_text": "Castle-and-moat perimeter trust only", "is_correct": False},
                            {"choice_text": "MAC flooding", "is_correct": False},
                            {"choice_text": "War driving", "is_correct": False},
                        ],
                    },
                    {
                        "question_text": (
                            "Administrators publish a cryptographic hash of a firmware file so "
                            "customers can detect whether the download was changed in transit. "
                            "Which security goal is this mainly supporting?"
                        ),
                        "difficulty": "easy",
                        "explanation": (
                            "A hash lets you detect unauthorized modification, which is integrity. "
                            "It does not hide the file (confidentiality) or keep a site online "
                            "(availability). Steganography hides data inside other data."
                        ),
                        "choices": [
                            {"choice_text": "Integrity", "is_correct": True},
                            {"choice_text": "Confidentiality", "is_correct": False},
                            {"choice_text": "Availability", "is_correct": False},
                            {"choice_text": "Steganography", "is_correct": False},
                        ],
                    },
                ],
            },
            "Security Operations": {
                "description": "SY0-701 Domain 4: monitoring, logging, and resilience",
                "questions": [
                    {
                        "question_text": (
                            "Security analysts need one place to collect logs from firewalls, "
                            "endpoints, and identity systems and to correlate alerts. Which "
                            "capability is that?"
                        ),
                        "difficulty": "medium",
                        "explanation": (
                            "A SIEM aggregates and correlates logs for detection and investigation. "
                            "MDM manages devices. A WAF protects web apps at the edge. DHCP "
                            "assigns IP addresses."
                        ),
                        "choices": [
                            {"choice_text": "SIEM", "is_correct": True},
                            {"choice_text": "Mobile device management (MDM) only", "is_correct": False},
                            {"choice_text": "A web application firewall (WAF) only", "is_correct": False},
                            {"choice_text": "DHCP", "is_correct": False},
                        ],
                    },
                    {
                        "question_text": (
                            "Ransomware encrypted file servers and also reached the backup share "
                            "on the same network. Which extra control would most improve recovery?"
                        ),
                        "difficulty": "medium",
                        "explanation": (
                            "Backups that are offline, air-gapped, or immutable cannot be "
                            "encrypted by the same outbreak. More antivirus on the already-reachable "
                            "backup share, longer passwords, or disabling MFA do not give you a "
                            "clean recovery copy."
                        ),
                        "choices": [
                            {
                                "choice_text": "Offline or immutable backups isolated from the production network",
                                "is_correct": True,
                            },
                            {
                                "choice_text": "Install another antivirus product on the same backup share",
                                "is_correct": False,
                            },
                            {"choice_text": "Require longer passwords and nothing else", "is_correct": False},
                            {"choice_text": "Disable MFA to speed restore work", "is_correct": False},
                        ],
                    },
                ],
            },
            "Security Program Management": {
                "description": "SY0-701 Domain 5: governance, access policy, and after-action work",
                "questions": [
                    {
                        "question_text": (
                            "A finance clerk can view invoices but cannot approve payments or "
                            "change vendor bank details. Which principle is this?"
                        ),
                        "difficulty": "easy",
                        "explanation": (
                            "Least privilege grants only the access required for the job. "
                            "Security through obscurity hides controls instead of restricting "
                            "rights. Implicit deny is a firewall default, not this HR/access "
                            "design. Job rotation is moving people between roles over time."
                        ),
                        "choices": [
                            {"choice_text": "Least privilege", "is_correct": True},
                            {"choice_text": "Security through obscurity", "is_correct": False},
                            {"choice_text": "Implicit deny as a job title", "is_correct": False},
                            {"choice_text": "Job rotation", "is_correct": False},
                        ],
                    },
                    {
                        "question_text": (
                            "After a phishing incident is contained, the team writes what failed, "
                            "what worked, and what will change in training and controls. What is "
                            "this activity called?"
                        ),
                        "difficulty": "easy",
                        "explanation": (
                            "Lessons learned (an after-action review) captures improvements while "
                            "the event is fresh. A tabletop is a discussion exercise, not the "
                            "write-up after a real incident. A warm site is a recovery facility. "
                            "A Faraday cage blocks radio signals."
                        ),
                        "choices": [
                            {"choice_text": "Lessons learned / after-action review", "is_correct": True},
                            {"choice_text": "A tabletop exercise", "is_correct": False},
                            {"choice_text": "Standing up a warm site", "is_correct": False},
                            {"choice_text": "Installing a Faraday cage", "is_correct": False},
                        ],
                    },
                ],
            },
        },
    },
    {
        "name": "Project Management Professional (PMP)",
        "provider": "Project Management Institute",
        "description": (
            "Original practice items mapped to the PMP Examination Content Outline "
            "domains: People, Process, and Business Environment."
        ),
        "source_url": PMP_GUIDE,
        "topics": {
            "People": {
                "description": "PMP ECO Domain 1: leadership, stakeholders, and conflict",
                "questions": [
                    {
                        "question_text": (
                            "A project manager focuses on removing blockers, coaching the team, "
                            "and sharing decision making instead of issuing task-level orders. "
                            "Which leadership approach is this?"
                        ),
                        "difficulty": "easy",
                        "explanation": (
                            "Servant leadership puts the team's needs and ability to deliver "
                            "first. Command-and-control and micromanagement centralize orders. "
                            "Gold plating is adding extra scope the customer did not ask for."
                        ),
                        "choices": [
                            {"choice_text": "Servant leadership", "is_correct": True},
                            {"choice_text": "Command-and-control leadership", "is_correct": False},
                            {"choice_text": "Micromanagement", "is_correct": False},
                            {"choice_text": "Gold plating", "is_correct": False},
                        ],
                    },
                    {
                        "question_text": (
                            "Late in planning you discover a regulator who can delay go-live and "
                            "was not in the original stakeholder list. What should you do first?"
                        ),
                        "difficulty": "medium",
                        "explanation": (
                            "New influential stakeholders belong in the stakeholder register and "
                            "need an engagement approach. Ignoring them until closing is late. "
                            "A risk entry may follow, but identification and engagement planning "
                            "come first. The sponsor is not 'fired' for a missed stakeholder."
                        ),
                        "choices": [
                            {
                                "choice_text": "Update the stakeholder register and plan how to engage them",
                                "is_correct": True,
                            },
                            {"choice_text": "Wait until closing to mention them in the final report", "is_correct": False},
                            {
                                "choice_text": "Only add a risk and do not change stakeholder artifacts",
                                "is_correct": False,
                            },
                            {"choice_text": "Remove the sponsor from the project", "is_correct": False},
                        ],
                    },
                    {
                        "question_text": (
                            "Two senior engineers disagree on a design, stand-ups have become "
                            "arguments, and delivery is slipping. What should the project manager "
                            "do first?"
                        ),
                        "difficulty": "medium",
                        "explanation": (
                            "The PM should facilitate conflict resolution so the team can decide "
                            "and resume work. Making both people the sponsor is not a conflict "
                            "technique. Canceling the project or ignoring the conflict does not "
                            "restore delivery."
                        ),
                        "choices": [
                            {
                                "choice_text": "Facilitate a structured discussion to resolve the conflict",
                                "is_correct": True,
                            },
                            {"choice_text": "Appoint both engineers as project sponsor", "is_correct": False},
                            {"choice_text": "Cancel the project immediately", "is_correct": False},
                            {"choice_text": "Ignore the conflict so it does not escalate", "is_correct": False},
                        ],
                    },
                ],
            },
            "Process": {
                "description": "PMP ECO Domain 2: delivery approach, change, cost, and risk",
                "questions": [
                    {
                        "question_text": (
                            "Earned value analysis shows CPI = 0.82 and SPI = 1.05. How is the "
                            "project performing?"
                        ),
                        "difficulty": "medium",
                        "explanation": (
                            "CPI below 1.0 means more cost was spent than the value earned (over "
                            "budget). SPI above 1.0 means the work is ahead of the schedule "
                            "baseline. CPI is a cost index, not a schedule index."
                        ),
                        "choices": [
                            {"choice_text": "Over budget and ahead of schedule", "is_correct": True},
                            {"choice_text": "Under budget and behind schedule", "is_correct": False},
                            {"choice_text": "Under budget and ahead of schedule", "is_correct": False},
                            {"choice_text": "CPI does not relate to cost performance", "is_correct": False},
                        ],
                    },
                    {
                        "question_text": (
                            "A key vendor might fail to deliver a component. Which response "
                            "transfers the financial impact to another party?"
                        ),
                        "difficulty": "easy",
                        "explanation": (
                            "Transfer shifts impact (often via insurance or a contract clause) "
                            "to a third party. Mitigation reduces probability or impact. Avoidance "
                            "removes the risk (for example, dropping the feature). Exploit is an "
                            "opportunity response, not a threat transfer."
                        ),
                        "choices": [
                            {
                                "choice_text": "Buy insurance or write a contract that assigns that loss to the vendor",
                                "is_correct": True,
                            },
                            {
                                "choice_text": "Add extra testing to reduce the chance of defects only",
                                "is_correct": False,
                            },
                            {
                                "choice_text": "Remove the feature so the vendor is no longer needed",
                                "is_correct": False,
                            },
                            {"choice_text": "Exploit the risk as a positive opportunity", "is_correct": False},
                        ],
                    },
                    {
                        "question_text": (
                            "On a predictive project, a customer asks for new scope after the "
                            "baseline is approved. What should the project manager do?"
                        ),
                        "difficulty": "easy",
                        "explanation": (
                            "Integrated change control evaluates impact on scope, schedule, cost, "
                            "and risk before the baseline changes. Implementing the request "
                            "immediately, waiting until closing, or only writing lessons learned "
                            "skips that control."
                        ),
                        "choices": [
                            {
                                "choice_text": "Submit a change request through integrated change control",
                                "is_correct": True,
                            },
                            {"choice_text": "Have the team start the new work immediately", "is_correct": False},
                            {"choice_text": "Wait until closing and then add the work", "is_correct": False},
                            {"choice_text": "Record it only in lessons learned", "is_correct": False},
                        ],
                    },
                    {
                        "question_text": (
                            "Product requirements are unclear and stakeholders expect them to "
                            "change every sprint. Which approach is the better fit?"
                        ),
                        "difficulty": "easy",
                        "explanation": (
                            "Adaptive / agile delivery expects evolving requirements and frequent "
                            "feedback. A rigid single-pass waterfall plan fights that change. "
                            "Skipping a backlog or daily coordination removes the tools that "
                            "make adaptive work visible."
                        ),
                        "choices": [
                            {"choice_text": "An adaptive (agile) delivery approach", "is_correct": True},
                            {
                                "choice_text": "A single frozen waterfall plan with no further change",
                                "is_correct": False,
                            },
                            {"choice_text": "No product backlog or prioritized work list", "is_correct": False},
                            {"choice_text": "Cancel all regular team coordination", "is_correct": False},
                        ],
                    },
                ],
            },
            "Business Environment": {
                "description": "PMP ECO Domain 3: compliance, benefits, and organizational context",
                "questions": [
                    {
                        "question_text": (
                            "The project delivered on the baseline date, but the business never "
                            "adopted the product and the expected revenue did not appear. Which "
                            "gap is this?"
                        ),
                        "difficulty": "medium",
                        "explanation": (
                            "Benefits realization is whether the organization actually obtains "
                            "the intended value, not only whether outputs were delivered on time. "
                            "Gold plating is extra unused scope. Crashing and fast tracking are "
                            "schedule-compression techniques."
                        ),
                        "choices": [
                            {"choice_text": "Benefits realization", "is_correct": True},
                            {"choice_text": "Gold plating", "is_correct": False},
                            {"choice_text": "Schedule crashing", "is_correct": False},
                            {"choice_text": "Fast tracking", "is_correct": False},
                        ],
                    },
                    {
                        "question_text": (
                            "A new regulation will make the current design non-compliant before "
                            "the planned launch. What should the project manager do first?"
                        ),
                        "difficulty": "medium",
                        "explanation": (
                            "External compliance changes are assessed for impact, then plans and "
                            "baselines are updated through change control as needed. Ignoring the "
                            "rule, changing branding only, or closing without analysis does not "
                            "protect the organization."
                        ),
                        "choices": [
                            {
                                "choice_text": "Assess the compliance impact and update project plans as required",
                                "is_correct": True,
                            },
                            {"choice_text": "Ignore the regulation until after launch", "is_correct": False},
                            {"choice_text": "Change only the product logo", "is_correct": False},
                            {
                                "choice_text": "Close the project immediately without impact analysis",
                                "is_correct": False,
                            },
                        ],
                    },
                    {
                        "question_text": (
                            "Two projects share the same specialist, and both schedules assume "
                            "that person is full time. What should you do?"
                        ),
                        "difficulty": "medium",
                        "explanation": (
                            "Overallocation is a resource conflict: level the work or renegotiate "
                            "priorities with sponsors. Hidden overtime as the only plan is unsustainable. "
                            "Deleting the charter or ignoring the calendar does not resolve the constraint."
                        ),
                        "choices": [
                            {
                                "choice_text": "Resource-level the work or renegotiate priorities with sponsors",
                                "is_correct": True,
                            },
                            {
                                "choice_text": "Assume undocumented overtime will cover both plans",
                                "is_correct": False,
                            },
                            {"choice_text": "Delete one project's charter without discussion", "is_correct": False},
                            {"choice_text": "Leave both schedules unchanged", "is_correct": False},
                        ],
                    },
                ],
            },
        },
    },
]


def _now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _get_or_create_exam(db, spec):
    exam = db.query(Exam).filter(Exam.name == spec["name"]).first()
    if exam is None:
        exam = Exam(
            name=spec["name"],
            provider=spec["provider"],
            description=spec["description"],
            created_at=_now(),
        )
        db.add(exam)
        db.flush()
    else:
        exam.provider = spec["provider"]
        exam.description = spec["description"]
    return exam


def _get_or_create_topic(db, exam, name, description):
    topic = (
        db.query(Topic)
        .filter(Topic.exam_id == exam.id, Topic.name == name)
        .first()
    )
    if topic is None:
        topic = Topic(exam_id=exam.id, name=name, description=description)
        db.add(topic)
        db.flush()
    else:
        topic.description = description
    return topic


def seed_exam_bank(db):
    """Insert missing exams, topics, and original questions. Safe to re-run."""
    created_questions = 0

    for spec in BANK:
        exam = _get_or_create_exam(db, spec)
        for topic_name, topic_spec in spec["topics"].items():
            topic = _get_or_create_topic(db, exam, topic_name, topic_spec["description"])
            for item in topic_spec["questions"]:
                existing = (
                    db.query(Question)
                    .filter(Question.question_text == item["question_text"])
                    .first()
                )
                if existing is not None:
                    continue

                question = Question(
                    exam_id=exam.id,
                    topic_id=topic.id,
                    question_text=item["question_text"],
                    difficulty=item["difficulty"],
                    explanation=item["explanation"],
                    created_at=_now(),
                    source_type=SOURCE_TYPE,
                    source_name=SOURCE_NAME,
                    source_url=spec["source_url"],
                    license=LICENSE,
                )
                db.add(question)
                db.flush()
                for choice in item["choices"]:
                    db.add(
                        QuestionChoice(
                            question_id=question.id,
                            choice_text=choice["choice_text"],
                            is_correct=choice["is_correct"],
                        )
                    )
                created_questions += 1

    db.commit()
    return created_questions
