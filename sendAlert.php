<?php

require __DIR__ . '/vendor/autoload.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

// Get the image path passed from Python
$attachment = $argv[1] ?? null;

$email = "example@gmail.com"; #enter recieving email here
$name  = "Camera3";

$mail = new PHPMailer(true);
try {
    $mail->isSMTP();
    $mail->Host       = 'smtp-relay.brevo.com';
    $mail->SMTPAuth   = true;
    $mail->Username   = 'example@smtp-brevo.com'; # uses brevo API
    $mail->Password   = 'Hashed_Password'; # uses brovo API
    $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
    $mail->Port       = 587;

    $mail->setFrom('example@gmail.com', 'enter_title'); # enter Sending email here, Title Name
    $mail->addAddress($email, $name);

    $mail->Subject = "Motion Detected";
    $mail->Body    = "Motion was detected. See the attached image.";

    // Attach the image if it exists
    if ($attachment && file_exists($attachment)) {
        $mail->addAttachment($attachment);
    }

    $mail->send();
    echo "Email sent successfully.\n";
} catch (Exception $e) {
    echo "Email failed: {$mail->ErrorInfo}\n";
}