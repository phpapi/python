<?php

class Spam {
  //name
  static function check_words($text, $name='all') {
    // TODO: config this url
    $url = "http://192.168.133.100:8888/check/$name";

    $request_params = array(
        "words" => $text
      );

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, false);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($request_params));

    $response = curl_exec($ch);
    curl_close($ch);

    return $response;
  }
}


# print_r(Spam::check_words("ni tmd stupid"));
