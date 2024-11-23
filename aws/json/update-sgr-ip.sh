GITPOD_IP=$(curl ifconfig.me)

echo "GITPOD_IP IS: ${GITPOD_IP}"

aws ec2 modify-security-group-rules \
    --group-id $DB_SG_ID \
    --security-group-rules "SecurityGroupRuleId=${DB_SG_RULE_ID},SecurityGroupRule={IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=${GITPOD_IP}/32}"

